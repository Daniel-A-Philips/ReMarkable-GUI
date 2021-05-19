import os
import PySimpleGUI as sg
import subprocess
import pygame
from multiprocessing import pool
from threading import Thread

def screens():
    pygame.display.init()
    numMon = pygame.display.get_num_displays()
    return [i for i in (0,numMon-1)]

def make_bitseq(s):
     return " ".join(f"{ord(i):08b}" for i in s)

def evdev_popup():
    popup_layout = [
                    [sg.Text('Please enter your root password to activate pressure sensitivity')],
                    [sg.Input('Root',size=(20,1),key='root'),sg.Button('Enter')]
                    ]
    popup_window = sg.Window('Root password',popup_layout)
    while True:
        event, values = popup_window.read()
        if event == 'Enter':
            return values['root']

def make_string(s):
     splits = s.split(" ")
     letters = []
     for a in splits:
         if a == '': continue
         letters.append(chr(int(a,2)))
     finalSTR = ""
     for lttr in letters:
         finalSTR = finalSTR + lttr
     return finalSTR

global layout
screenData = screens()
layout = [
         [sg.Text('IP Address',size=(9,1)),sg.Input("IP",size=(14,1),key='IP'),sg.Button("Load IP")],
         [sg.Text('Password',size=(9,1)),sg.Input("Password",size=(14,1),key='password'),sg.Button("Load Password")],
         [sg.Text('Orientation',size=(9,1)),sg.Combo(['Bottom','Top','Left','Right'],default_value = 'Bottom',key='orientation')],
         [sg.Text('Monitor',size=(9,1)),sg.Combo(screenData, default_value = screenData[0],key='monitor')],
         [sg.Text('Status: Disconnected',key='status')],
         [sg.Checkbox("Evdev (Only on Linux)", False,key='evdev'), sg.Checkbox("Save Password?",False,key='save')],
         [sg.Button("Run"),sg.Button("Stop")],
         [sg.Button("Quit"),sg.Text('This will end any ReMouse sessions running')]
         ]
iconPath = os.path.dirname(os.path.abspath(__file__))+'/logo.png'
window = sg.Window("ReMouse GUI",layout)
window.set_icon(iconPath)

def run(values):
    while "/" in values['orientation']: values['orientation'] = values['orientation'][:-1]
    values['orientation'] = values['orientation'].lower()
    values['monitor'] = values['monitor']
    print('Values:', values)
    cmd = "remouse --address " + values['IP'] + " --password " + values['password'] + " --orientation " + values['orientation'] + " --monitor " + str(values['monitor'])
    if values['save']:
        File = open("data.txt",'w')
        readFile = open("data.txt",'r')
        read = readFile.read()
        toWrite = make_bitseq(values['IP'] + "," + values['password'] + "," + values['orientation'] + "," + values['monitor'] + "/") #The slash is added to indicate the end of this data
        if toWrite in read:
            return cmd
        File.write(toWrite)
        File.close()
    if values['evdev']:
        cmd = cmd + " --evdev"
    return cmd

def loadData():
    File = open("data.txt","r")
    lines = File.read()
    lines = lines.split("/")
    if '' in lines:
        lines.remove(len(lines))
    if len(lines) == 1:
        read = lines[0]
        readString = make_string(read).split(",")
        values['IP'] = readString[0]
        values['password'] = readString[1]
        values['orientation'] = readString[2].lower()
        values['monitor'] = readString[3]
    return values

def kill():
    os.system('pkill remouse')

while True:
    event, values = window.read()
    print(values)
    cmd = ""
    if event == "Run":
        kill()
        numChoice = 1
        cmd = run(values)
        #sudo_pswd = evdev_popup()
        thread = Thread(target = lambda: os.system(cmd))
        thread.start()
        print('Started Thread:',cmd)
        window['status'].update('Status: Connected')
    elif event == "Stop":
        kill()
    elif event == "Load IP":
        values = loadData()
        window['IP'].update(values['IP'])
    elif event == "Load Password":
        values = loadData()
        window['password'].update(values['password'])
    else:
        kill()
        window.close()
        exit()





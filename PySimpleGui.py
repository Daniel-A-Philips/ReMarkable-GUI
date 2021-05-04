import os
import PySimpleGUI as sg
import subprocess
from multiprocessing import pool
from threading import Thread

def screens():
    output = [l for l in subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()]
    return [l.split()[0] for l in output if " connected " in l]

def make_bitseq(s):
     return " ".join(f"{ord(i):08b}" for i in s)

def make_string(s):
     splits = s.split(" ")
     print(splits)
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
         [sg.Text('Monitor',size=(9,1)),sg.Combo(screens(), default_value = screens()[0],key='monitor')],
         [sg.Text('Status: Disconnected',key='status')],
         [sg.Checkbox("Evdev (Only on Linux)", False,key='evdev'), sg.Checkbox("Save Password?",False,key='save')],
         [sg.Button("Run"), sg.Button("Run using saved data")],
         [sg.Button("Quit"),sg.Text('This will end any ReMouse sessions running')]
         ]

window = sg.Window("ReMouse GUI",layout,icon= os.path.dirname(os.path.abspath(__file__))+'logo.svg')

def run(values):
    while "/" in values['orientation']: values['orientation'] = values['orientation'][:-1]
    values['orientation'] = values['orientation'].lower()
    values['monitor'] = values['monitor']
    print('Values:', values)
    cmd = "remouse --address " + values['IP'] + " --password " + values['password'] + " --orientation " + values['orientation'] + " --monitor " + str(screens().index(values['monitor']))
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
        cmd += " --evdev"
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

def runWithSavedData(values):
    values = loadData()
    return run(values)

while True:
    event, values = window.read()
    cmd = ""
    if event == "Run":
        os.system("pkill remouse")
        numChoice = 1
        cmd = run(values)
        thread = Thread(target = lambda: os.system(cmd))
        thread.start()
        window['status'].update('Status: Connected')

    elif event == "Run using saved data":
        os.system("pkill remouse")
        cmd = runWithSavedData(values)
        thread = Thread(target = lambda: os.system(cmd))
        thread.start()
        window['status'].update('Status: Connected')

    elif event == "Load IP":
        values = loadData()
        window['IP'].update(values['IP'])
    elif event == "Load Password":
        values = loadData()
        window['password'].update(values['password'])
    else:
        os.system("pkill remouse")
        window.close()
        exit()





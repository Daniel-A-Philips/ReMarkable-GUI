import tkinter as tk
from threading import Thread
import os
import subprocess


class TKint:

    def screens(self):
        output = [l for l in subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()]
        return [l.split()[0] for l in output if " connected " in l]

    def make_bitseq(self,s):
        return " ".join(f"{ord(i):08b}" for i in s)

    def make_string(self,s):
        splits = s.split(" ")
        print(splits)
        letters = []
        for a in splits:
            if a == '': continue
            letters.append(chr(int(a, 2)))
        finalSTR = ""
        for lttr in letters:
            finalSTR = finalSTR + lttr
        return finalSTR

    def arrayToString(self,s):
        readString = self.make_string(s)[:-1].split(",")
        print("readString:",readString)
        self.ip = readString[0]
        self.pswd = readString[1]
        self.orientation = readString[2]
        self.monitor = readString[3]
        self.String = self.ip + "," + self.pswd + "," + self.orientation + "/"
        return readString

    ## Values = [IP:String,Password:String,Orientation:String, Monitor Number:Integer,Evdev:Boolean,Save Password:Boolean]
    global data
    def runNewData(self,values):
        os.system("pkill remouse")
        print('Values:', values)
        while "/" in values[2]: values[2] = values[2][:-1]
        values[2] = values[2].lower()
        print(values[3])
        values[3] = self.screenData.index(values[3])
        cmd = "remouse --address " + values[0] + " --password " + values[1] + " --orientation " + values[2] + " --monitor " + str(values[3])
        print(values)
        if values[5] == 1:
            File = open("data.txt", 'w')
            readFile = open("data.txt", 'r')
            read = readFile.read()
            toWrite = self.make_bitseq(values[0] + "," + values[1] + "," + values[2] + "," + str(values[3]) + "/")  # The slash is added to indicate the end of this data
            if toWrite in read:
                return cmd
            File.write(toWrite)
            File.close()
        if values[4] == 1:
            cmd += " --evdev"
        thread = Thread(target= lambda: os.system(cmd))
        thread.start()
        return cmd

    def exit(self):
        os.system("pkill remouse")
        exit()

    ## Values = [IP:String,Password:String,Orientation:String, Monitor Number:Integer,Evdev:Boolean,Save Password:Boolean]
    def runWithSavedData(self,values):
        os.system("pkill remouse")
        File = open("data.txt", "r")
        lines = File.read()
        lines = lines.split("/")
        while '' in lines:
            lines.remove(lines)
        if len(lines) == 1:
            self.arrayToString(lines[0])
            values[0] = self.ip
            values[1] = self.pswd
            values[2] = self.orientation
            valuese[3] = self.monitor
            self.cmd = self.runNewData(values)
            print(self.cmd)

    def __init__(self, master=None):
        self.os = os
        # build ui
        self.frame1 = tk.Frame(master)
        self.IPLabel = tk.Label(self.frame1)
        self.IPLabel.configure(text='IP Address')
        self.IPLabel.pack(side='top')
        self.IPEntry = tk.Entry(self.frame1)
        _text_ = '''IP Address'''
        self.IPEntry.delete('0', 'end')
        self.IPEntry.insert('0', _text_)
        self.IPEntry.pack(side='top')
        self.PasswordLabel = tk.Label(self.frame1)
        self.PasswordLabel.configure(text='Password')
        self.PasswordLabel.pack(side='top')
        self.PasswordEntry = tk.Entry(self.frame1)
        _text_ = '''Password'''
        self.PasswordEntry.delete('0', 'end')
        self.PasswordEntry.insert('0', _text_)
        self.PasswordEntry.pack(side='top')
        self.OrientationLabel = tk.Label(self.frame1)
        self.OrientationLabel.configure(text='Orientation')
        self.OrientationLabel.pack(side='top')
        __orVar = tk.StringVar(value='Bottom')
        __orValues = ["Left","Right","Top","Bottom"]
        self.OrientationMenu = tk.OptionMenu(self.frame1, __orVar, *__orValues, command = None)
        self.OrientationMenu.pack(anchor='center', expand='true', side='top')
        self.ScreenLabel = tk.Label(self.frame1)
        self.ScreenLabel.configure(text='Monitor')
        self.ScreenLabel.pack(side='top')
        self.screenData = self.screens()
        __monVar = tk.StringVar(value=self.screenData[0])
        __monValues = self.screenData
        self.ScreenMenu = tk.OptionMenu(self.frame1, __monVar, *__monValues, command = None)
        self.ScreenMenu.pack(anchor='center', expand='true', side='top')
        self.EvdevInt = tk.IntVar()
        self.Evdev = tk.Checkbutton(self.frame1,variable=self.EvdevInt)
        self.Evdev.configure(text='Use pressure (only on Linux)')
        self.Evdev.pack(side='top')
        self.SaveDataInt = tk.IntVar()
        self.SaveData = tk.Checkbutton(self.frame1,variable = self.SaveDataInt)
        self.SaveData.configure(text='Save Data?')
        self.SaveData.pack(side='top')
        self.RunSavedData = tk.Button(self.frame1, command=lambda: self.runWithSavedData([self.IPEntry.get(),self.PasswordEntry.get(),__orVar.get(),__monVar.get(),self.EvdevInt.get(),self.SaveDataInt.get()]))
        self.RunSavedData.configure(text='Run with saved data')
        self.RunSavedData.pack(side='top')
        self.Run = tk.Button(self.frame1,command=lambda: self.runNewData([self.IPEntry.get(),self.PasswordEntry.get(),__orVar.get(),__monVar.get(),self.EvdevInt.get(),self.SaveDataInt.get()]))
        self.Run.configure(text='Run')
        self.Run.pack(side='top')
        self.Exit = tk.Button(self.frame1,command=lambda: self.exit())
        self.Exit.configure(text='Exit')
        self.Exit.pack(side='top')
        self.frame1.configure(height='200', width='200')
        self.frame1.pack(side='top')

        # Main widget
        self.mainwindow = self.frame1

    def run(self):
        print("run")
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = TKint(root)
    app.run()



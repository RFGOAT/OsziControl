import tkinter as tk
from tkinter import filedialog
import OsziControlLib as OsziLib
import serial as COMPort

def KeyboardControl():
    FileDialogFlag = False
    while True:
        command = int( input() )
        if command == 1:
            print("Auto")
            OsziLib.SetTrigger('auto')
        elif command == 2:
            print('Normal')
            OsziLib.SetTrigger('normal')
        elif command == 3:
            print('STOP')
            OsziLib.SetTrigger('stop')
        elif command == 4:
            print('STOP')
            OsziLib.SetTrigger('single')
        elif command == 5:
            if FileDialogFlag == False:
                FileDialogFlag = True
                FileSaveDir = filedialog.askdirectory(initialdir = "C:")
            OsziLib.Screenshot(FileSaveDir)
        else:
            print('Button not supported')
                   
       
def FS_Control():
    FileDialogFlag = False
    while True:
        x = FloorSwitch.read()
        k = str(x)
        try:
            command = int(k[2])
            if command == 1:
                print("Auto")
                OsziLib.SetTrigger('auto')
            elif command == 2:
                print('Normal')
                OsziLib.SetTrigger('normal')
            elif command == 3:
                print('STOP')
                OsziLib.SetTrigger('stop')
            elif command == 4:
                print('STOP')
                OsziLib.SetTrigger('stop')
            elif command == 5:
                print('Single')
                OsziLib.SetTrigger('single')
                if FileDialogFlag == False:
                    FileDialogFlag = True
                    FileSaveDir = filedialog.askdirectory(initialdir = "C:")
                OsziLib.Screenshot(FileSaveDir)
            elif command == 6:
                print('No Command')
            else:
                print('Something went wrong with the Floor-Switch')
        except Exception:
            k = k # Dummy

######################################################################################
######################################################################################
#Start
######################################################################################  
root = tk.Tk()
root.withdraw()   

#Open Serial COM Port or Keyboard Control
SerialPort = 'COM12'
try:        
    FloorSwitch = COMPort.Serial(SerialPort, 9600, timeout=1)
    print('--floor switch enabled--\n')
    FS_Control() 
except Exception:
    print("Unable to connect to floor switch at " + SerialPort + "Keyboard Control Active")
    KeyboardControl()










import visa
import sys
import serial
import time
import os
import tkinter as tk
from tkinter import filedialog
#import OsziControlLib as OsziLib


    
def Screenshot(FileSaveDir):
     
    Trigger = str(MyOszi.query("TRMD?"))
    MyOszi.write("TRMD STOP")
    MyOszi.write("SCDP") # Send Screendump Command
    data = MyOszi.read_raw() # get screen data
    MyOszi.write(Trigger)

    # write it to file counter screenshot index
    for i in range(0,50):
        FullFilePath = FileSaveDir + '/Screenshot%d.png' %i
        if not os.path.exists(FullFilePath):
            newfile=open(FullFilePath,'wb')
            newfile.write(data)
            newfile.close()
            break
        
    print('Screenshot saved as:  ' + 'Screenshot%d.png' %i)


def Control():
    
    FileDialogFlag = False
    
    while True:
        command = int( input() )
        if command == 1:
            print("Auto")
            MyOszi.write("TRMD AUTO")
        elif command == 2:
            print('Normal')
            MyOszi.write("TRMD NORMAL")
        elif command == 3:
            print('STOP')
            MyOszi.write("TRMD STOP")
        elif command == 4:
            print('STOP')
            MyOszi.write("TRMD STOP")
        elif command == 5:
            MyOszi.write("TRMD STOP")
            if FileDialogFlag == False:
                FileDialogFlag = True
                FileSaveDir = filedialog.askdirectory(initialdir = "C:")
            Screenshot(FileSaveDir)
        else:
            print('Button not supported')
                   
       
def ControlSerial():
    
    FileDialogFlag = False
    
    while True:
        x = FloorSwitch.read()
        k = str(x)
        
        try:
            command = int(k[2])
            if command == 1:
                print("Auto")
                MyOszi.write("TRMD AUTO")
            elif command == 2:
                print('Normal')
                MyOszi.write("TRMD NORMAL")
            elif command == 3:
                print('STOP')
                MyOszi.write("TRMD STOP")
            elif command == 4:
                print('STOP')
                MyOszi.write("TRMD STOP")
            elif command == 5:
                MyOszi.write("TRMD STOP")
                if FileDialogFlag == False:
                    FileDialogFlag = True
                    FileSaveDir = filedialog.askdirectory(initialdir = "C:")
                Screenshot(FileSaveDir)
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

GLOBAL_TOUT =  20000   
#Get VISA Ressource  
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') 
SCOPE_VISA_ADDRESS = str(rm.list_resources())
SCOPE_VISA_ADDRESS = SCOPE_VISA_ADDRESS[2:-3]
try:
    MyOszi = rm.open_resource(SCOPE_VISA_ADDRESS)
    print("Connected to oscilloscope at:")
    print(str(SCOPE_VISA_ADDRESS) + " \n")
except Exception:
    print("Unable to connect to oscilloscope at " + str(SCOPE_VISA_ADDRESS) + ". Aborting script.\n")
    time.sleep(5)
    sys.exit()
    
#Initialize Oszilloscope
MyOszi.timeout = GLOBAL_TOUT
time.sleep(3) 
MyOszi.clear()
IDN = str(MyOszi.query("*IDN?"))
print("Oscilloscope ID:")
print(IDN + " \n")

#Open Serial COM Port or Keyboard Control
SerialPort = 'COM12'
try:        
    FloorSwitch = serial.Serial(SerialPort, 9600, timeout=1)
    print('--floor switch enabled--\n')
    ControlSerial() 
except Exception:
    print("Unable to connect to floor switch at " + SerialPort + "Keyboard Control Active")
    Control()










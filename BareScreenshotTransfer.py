# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:39:40 2017

@author: U2683327
"""

import visa
import sys
import numpy as np
import time
import os
import tkinter as tk
from tkinter import filedialog

    

def Screenshot(saveDir):
     
    MSOX4024A.write(":STOP")
    # configure ink saver (black background as seen on screen)
    MSOX4024A.write(':HARDcopy:INKSaver 0')
    # get screen data
    data = MSOX4024A.query_binary_values(':DISPlay:DATA? PNG, COLOR', datatype='B')
    MSOX4024A.write(":RUN")

    
    # write it to file counter screenshot index
    for i in range(0,50):
        ScreenshotFilePath = saveDir + '/Screenshot%d.png' %i
        if not os.path.exists(ScreenshotFilePath):
            newfile=open(ScreenshotFilePath,'wb')
            newfile.write(bytearray(data))
            newfile.close()
            break
        
    print('Screenshot saved as:  ' + 'Screenshot%d.png' %i)




######################################################################################
######################################################################################
#Start
######################################################################################  
root = tk.Tk()
root.withdraw()   
#VISA-Ressource
GLOBAL_TOUT =  20000     
#SCOPE_VISA_ADDRESS = "USB0::0x0957::0x17B6::MY56310539::0::INSTR" 
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') 

SCOPE_VISA_ADDRESS = str(rm.list_resources())
SCOPE_VISA_ADDRESS = SCOPE_VISA_ADDRESS[2:-3]

try:
    MSOX4024A = rm.open_resource(SCOPE_VISA_ADDRESS)
    print("Connected to oscilloscope at:")
    print(str(SCOPE_VISA_ADDRESS) + " \n")
except Exception:
    print("Unable to connect to oscilloscope at " + str(SCOPE_VISA_ADDRESS) + ". Aborting script.\n")
    time.sleep(5)
    sys.exit()

MSOX4024A.timeout = GLOBAL_TOUT
time.sleep(3) 
MSOX4024A.clear()
IDN = str(MSOX4024A.query("*IDN?"))
print("Oscilloscope ID:")
print(IDN + " \n")

FileDialogFlag = False
saveDir = ""

try:
    while True:
        text = input("Press ENTER for Screenshot-Transfer")
        
        if text == "":
            if FileDialogFlag==False:
                saveDir = filedialog.askdirectory()
                FileDialogFlag = True
            Screenshot(saveDir)
            time.sleep(3)
            
        else:
            time.sleep(3)
            print('\n--not a valid input--\n')          
    
    
except Exception:
    print('\n--Something went wrong--\n Aborting Script...')
    time.sleep(5)
    sys.exit()

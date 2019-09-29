#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 18:41:25 2019

@author: achim
"""
import visa
import sys
import time
import os



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

    
def InitOszi():
    #VISA-Ressource
    GLOBAL_TOUT =  20000        
    rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') 
    SCOPE_VISA_ADDRESS = str(rm.list_resources())
    SCOPE_VISA_ADDRESS = SCOPE_VISA_ADDRESS[2:-3]
    
    try:
        global MyOszi
        MyOszi = rm.open_resource(SCOPE_VISA_ADDRESS)
        print("Connected to oscilloscope at:")
        print(str(SCOPE_VISA_ADDRESS) + " \n")
    except Exception:
        print("Unable to connect to oscilloscope at " + str(SCOPE_VISA_ADDRESS) + ". Aborting script.\n")
        time.sleep(5)
        sys.exit()
    
    MyOszi.timeout = GLOBAL_TOUT
    time.sleep(3) 
    MyOszi.clear()
    IDN = str(MyOszi.query("*IDN?"))
    print("Oscilloscope ID:")
    print(IDN + " \n")
    
    
    
def SetTrigger(tm):
     if tm == 'auto':
         MyOszi.write("TRMD AUTO")
     elif tm == 'normal':
         MyOszi.write("TRMD NORM")
     elif tm == 'stop':
         MyOszi.write("TRMD STOP")
     elif tm == 'single':
         MyOszi.write("TRMD SINGLE")
     else:
         print('no valid trigger')




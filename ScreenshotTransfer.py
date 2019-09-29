# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:39:40 2017

@author: U2683327
"""
import sys
import time
import tkinter as tk
from tkinter import filedialog
import OsziControlLib as OsziLib


######################################################################################
######################################################################################
#Start
######################################################################################  
root = tk.Tk()
root.withdraw()

OsziLib.InitOszi()
 
try:
    FileDialogFlag = True
    while True:
        i = input("Press ENTER for Screenshot-Transfer")
        
        if i == "":
            if FileDialogFlag==False:
                FileSaveDir = filedialog.askdirectory()
                FileDialogFlag = True
            OsziLib.Screenshot(FileSaveDir)
            time.sleep(3)
        else:
            time.sleep(3)
            print('\n--not a valid input--\n')          
    
except Exception:
    print('\n--Something went wrong--\n Aborting Script...')
    time.sleep(5)
    sys.exit()


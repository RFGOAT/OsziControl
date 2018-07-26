# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 07:19:05 2017

@author: U2683327
"""
import sys
import visa # PyVisa info @ http://PyVisa.readthedocs.io/en/stable/
import numpy as np


USER_REQUESTED_POINTS = 10000
SCOPE_VISA_ADDRESS = "USB0::0x0957::0x17B6::MY56310539::0::INSTR"

GLOBAL_TOUT =  10000 # IO time out in milliseconds

## Save Locations
BASE_FILE_NAME = "OsziData"
BASE_DIRECTORY = "C:\\_Python\\"

rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # This uses PyVisa; PyVisa info @ http://PyVisa.readthedocs.io/en/stable/

try:
    MSOX4024A = rm.open_resource(SCOPE_VISA_ADDRESS)
except Exception:
    print ("Unable to connect to oscilloscope at " + str(SCOPE_VISA_ADDRESS) + ". Aborting script.\n")
    sys.exit()

MSOX4024A.timeout = GLOBAL_TOUT
MSOX4024A.clear()


## Get Number of analog channels on scope
#IDN = str(MSOX4024A.query("*IDN?"))
#print(IDN + '\n')




def TestRunState():
    
    OpeCondReg = int ( MSOX4024A.query(":OPERegister:CONDition?") )
    print( bin(OpeCondReg) )
    mask = 1 << 3 # Third Bit indicates Run/Stop state
    Test = OpeCondReg & mask
    
    if (Test != 0):
        return "Run"
    else:
        return "Stop"

print( TestRunState() )


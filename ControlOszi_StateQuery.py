import pyvisa
import sys
import serial
import numpy as np
import time
import os
import tkinter as tk
from tkinter import filedialog


TimeBaseLookUp = [          2.00E-09, 5.00E-09, 10.00E-09, 20.00E-09, 50.00E-09, 100.00E-09, 200.00E-09, 500.00E-09,
              1.00E-06, 2.00E-06, 5.00E-06, 10.00E-06, 20.00E-06, 50.00E-06, 100.00E-06, 200.00E-06, 500.00E-06,
              1.00E-03, 2.00E-03, 5.00E-03, 10.00E-03, 20.00E-03, 50.00E-03, 100.00E-03, 200.00E-03, 500.00E-03,
              1.00E-00, 2.00E-00, 5.00E-00, 10.00E-00, 20.00E-00, 50.00E-00]

    

    
    
    
def Screenshot(saveDir):
        
    # configure ink saver (black background as seen on screen)
    MSOX4024A.write(':HARDcopy:INKSaver 0')
    # get screen data
    data = MSOX4024A.query_binary_values(':DISPlay:DATA? PNG, COLOR', datatype='B')
    
    #create saving folder
    timeF = time.strftime("%d_%m_%y")
    ScShPath = saveDir #+ "/OsziData_" + timeF
    
    if not os.path.exists(ScShPath):
        os.makedirs(ScShPath)
    # write it to file counter screenshot index
    for i in range(0,50):
        ScreenshotFilePath = ScShPath + '/Screenshot%d.png' %i
        if not os.path.exists(ScreenshotFilePath):
            newfile=open(ScreenshotFilePath,'wb')
            newfile.write(bytearray(data))
            newfile.close()
            break
        
    print('Screenshot saved as:\n' + ScreenshotFilePath)#saveDir + '/' + 'Screenshot%d.png' %i)





def Control():
    
    FileDialogFlag = False
    
    while True:
        i = int( input() )
        if i==4:
            MSOX4024A.write(":RUN")
        elif i==1:
            MSOX4024A.write(":STOP")
        elif i==3:
            MSOX4024A.write(":SINGle")
        elif i==2:
            if FileDialogFlag == False:
                FileDialogFlag = True
                saveDir = filedialog.askdirectory()
            #print('Transfering Screenshot')
            Screenshot(saveDir)
        elif i==5:
            if FileDialogFlag == False:
                FileDialogFlag = True
                saveDir = filedialog.askdirectory()
            #print('Transfering Data')
            TransferData(saveDir)
        else:
            print('Button not supported')
            

def TestRunState():
    
    OpeCondReg = int ( MSOX4024A.query(":OPERegister:CONDition?") )
    mask = 1 << 3 # Third Bit indicates Run/Stop state
    Test = OpeCondReg & mask
    
    if (Test != 0):
        return "Run"
    else:
        return "Stop"
        
def AdjustTimeBase(direction):
   
    CurrScaleStr = str(MSOX4024A.query(":TIMebase:SCALe?"))
    CurrScale = float(CurrScaleStr[1:-1])
    index = TimeBaseLookUp.index(CurrScale)
    
    if direction == 'n':
        index = index - 1
    elif direction == 'w':
        index = index + 1
    MSOX4024A.write(":TIMebase:SCALe " + str(TimeBaseLookUp[index])  )  
        
def ControlSerial():
    
    SerialPort = 'COM12'
    
    try:
    
        FileDialogFlag = False
        
        with serial.Serial(SerialPort, 9600, timeout=1) as ser:
            
            print('--floor switch enabled--\n')
            
            while True:
                x = ser.read()
                
                k = str(x)
                
                try:
                    command = int(k[2])
                    state = TestRunState()
                    if command == 1:
                        if ( state == "Stop"):
                            print('Run')
                            MSOX4024A.write(":RUN")
                        if (state == "Run"):
                            print('Stop')
                            MSOX4024A.write(":STOP")
                    if command == 2:
                        print('Single')
                        MSOX4024A.write(":SINGle")
                    if command == 3:
                        if FileDialogFlag == False:
                            FileDialogFlag = True
                            saveDir = filedialog.askdirectory(initialdir = "C:\\Users\\U2683327\\Desktop")
                        MSOX4024A.write(":STOP")
                        Screenshot(saveDir)
                    if command == 4:
                        if FileDialogFlag == False:
                            FileDialogFlag = True
                            saveDir = filedialog.askdirectory()
                        MSOX4024A.write(":STOP")
                        TransferData(saveDir)
                    if command == 5:
                        AdjustTimeBase('w')
                        print('Widen Timebase')
                    if command == 6:
                        AdjustTimeBase('n')
                        print('Narrow Timebase')
    
                except Exception:
                    k = k # Dummy
    except Exception:
        print("Unable to connect to floor switch at " + SerialPort + "!\n\nAborting script.\n")
        time.sleep(5)
        sys.exit()

######################################################################################
######################################################################################
#Start
######################################################################################  
  
#VISA-Ressource
GLOBAL_TOUT =  20000     
SCOPE_VISA_ADDRESS = 'ASRL/dev/ttyAMA0::INSTR'
rm = pyvisa.ResourceManager()

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
#MSOX4024A.clear()
IDN = str(MSOX4024A.query("*IDN?"))
print("Oscilloscope ID:")
print(IDN + " \n")
MSOX4024A.write("*RST")
#print("ready\n")
# mode = 'f' #input('Press -k- for Keyboard operation or -f- for floor switch')

# if mode == 'k':
    # print("Press:")
    # print("4 -> Run")
    # print("1 -> Stop")
    # print("3 -> Single")
    # print("2 -> Transfer Screenshot to PC")
    # print("5 -> Transfer Data to PC")
    # Control()
# elif mode == 'f':
    # ControlSerial()
# else:
    # print('\n--not a valid mode--\n Aborting Script...')
    # time.sleep(5)
    # sys.exit()

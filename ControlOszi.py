import visa
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

    
def TransferData(saveDir):

    USER_REQUESTED_POINTS = 10000
#    NUMBER_ANALOG_CHS = int(MODEL[len(MODEL)-2])
    NUMBER_CHANNELS_ON = 0
    
    ## Note that this only has to be done once for repetitive acquisitions if the channel scales (and on/off) are not changed.
    MSOX4024A.write(":WAVeform:POINts:MODE MAX") # MAX mode works for all acquisition types, so this is done here to avoid Acq. Type vs points mode problems. Adjusted later for specific acquisition types.
    ## Channel 1
    On_Off = int(MSOX4024A.query(":CHANnel1:DISPlay?")) # Is the channel displayed? If not, don't pull.
    if On_Off == 1:
        Channel_Acquired = int(MSOX4024A.query(":WAVeform:SOURce CHANnel1;:WAVeform:POINts?"))  # The scope can acquire waveform data even if the channel is off (in some cases) - so modify as needed
            ## If this returns a zero, then this channel did not capture data and thus there are no points
            ## Note that setting the :WAV:SOUR to some channel has the effect of turning it on
    else:
        Channel_Acquired = 0
    if Channel_Acquired == 0:
        CHAN1_STATE = 0
        MSOX4024A.write(":CHANnel1:DISPlay OFF") # Setting a channel to be a waveform source turns it on... so if here, turn it off.
        NUMBER_CHANNELS_ON += 0
    else:
        CHAN1_STATE = 1
        NUMBER_CHANNELS_ON += 1
        if NUMBER_CHANNELS_ON == 1:
            FIRST_CHANNEL_ON = 1
        LAST_CHANNEL_ON = 1
        Pre = MSOX4024A.query(":WAVeform:SOURce CHANnel1;:WAVeform:PREamble?").split(',')
        Y_INCrement_Ch1 = float(Pre[7]) # Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
        Y_ORIGin_Ch1    = float(Pre[8]) # Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
        Y_REFerence_Ch1 = float(Pre[9]) # Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
    
    ## Channel 2
    On_Off = int(MSOX4024A.query(":CHANnel2:DISPlay?"))
    if On_Off == 1:
        Channel_Acquired = int(MSOX4024A.query(":WAVeform:SOURce CHANnel2;:WAVeform:POINts?"))
    else:
        Channel_Acquired = 0
    if Channel_Acquired == 0:
        CHAN2_STATE = 0
        MSOX4024A.write(":CHANnel2:DISPlay OFF")
        NUMBER_CHANNELS_ON += 0
    else:
        CHAN2_STATE = 1
        NUMBER_CHANNELS_ON += 1
        if NUMBER_CHANNELS_ON == 1:
            FIRST_CHANNEL_ON = 2
        LAST_CHANNEL_ON = 2
        Pre = MSOX4024A.query(":WAVeform:SOURce CHANnel2;:WAVeform:PREamble?").split(',')
        Y_INCrement_Ch2 = float(Pre[7])
        Y_ORIGin_Ch2    = float(Pre[8])
        Y_REFerence_Ch2 = float(Pre[9])
    
    ## Channel 3
    On_Off = int(MSOX4024A.query(":CHANnel3:DISPlay?"))
    if On_Off == 1:
        Channel_Acquired = int(MSOX4024A.query(":WAVeform:SOURce CHANnel3;:WAVeform:POINts?"))
    else:
        Channel_Acquired = 0
    if Channel_Acquired == 0:
        CHAN3_STATE = 0
        MSOX4024A.write(":CHANnel3:DISPlay OFF")
        NUMBER_CHANNELS_ON += 0
    else:
        CHAN3_STATE = 1
        NUMBER_CHANNELS_ON += 1
        if NUMBER_CHANNELS_ON == 1:
            FIRST_CHANNEL_ON = 3
        LAST_CHANNEL_ON = 3
        Pre = MSOX4024A.query(":WAVeform:SOURce CHANnel3;:WAVeform:PREamble?").split(',')
        Y_INCrement_Ch3 = float(Pre[7])
        Y_ORIGin_Ch3    = float(Pre[8])
        Y_REFerence_Ch3 = float(Pre[9])
    
    ## Channel 4
    On_Off = int(MSOX4024A.query(":CHANnel4:DISPlay?"))
    if On_Off == 1:
        Channel_Acquired = int(MSOX4024A.query(":WAVeform:SOURce CHANnel4;:WAVeform:POINts?"))
    else:
        Channel_Acquired = 0
    if Channel_Acquired == 0:
        CHAN4_STATE = 0
        MSOX4024A.write(":CHANnel4:DISPlay OFF")
        NUMBER_CHANNELS_ON += 0
    else:
        CHAN4_STATE = 1
        NUMBER_CHANNELS_ON += 1
        if NUMBER_CHANNELS_ON == 1:
            FIRST_CHANNEL_ON = 4
        LAST_CHANNEL_ON = 4
        Pre = MSOX4024A.query(":WAVeform:SOURce CHANnel4;:WAVeform:PREamble?").split(',')
        Y_INCrement_Ch4 = float(Pre[7])
        Y_ORIGin_Ch4    = float(Pre[8])
        Y_REFerence_Ch4 = float(Pre[9])
    
    ##no Channels available
    if NUMBER_CHANNELS_ON == 0:
        MSOX4024A.clear()
        MSOX4024A.close()
        sys.exit("No data has been acquired. Properly closing scope and aborting script.")
    
    ################################################################################################################
    ## Setup data export - For repetitive acquisitions, this only needs to be done once unless settings are changed
    MSOX4024A.write(":WAVeform:FORMat WORD") # 16 bit word format... or BYTE for 8 bit format - WORD recommended, see more comments below when the data is actually retrieved
        ## WORD format especially  recommended  for Average and High Res. Acq. Types, which can produce more than 8 bits of resolution.
    MSOX4024A.write(":WAVeform:BYTeorder LSBFirst") # Explicitly set this to avoid confusion - only applies to WORD FORMat
    MSOX4024A.write(":WAVeform:UNSigned 0") # Explicitly set this to avoid confusion
    ## Determine Acquisition Type to set points mode properly
    ACQ_TYPE = str(MSOX4024A.query(":ACQuire:TYPE?")).strip("\n")
            ## This can also be done when pulling pre-ambles (pre[1]) or may be known ahead of time, but since the script is supposed to find everything, it is done now.
    if ACQ_TYPE == "AVER" or ACQ_TYPE == "HRES": # Don't need to check for both types of mnemonics like this: if ACQ_TYPE == "AVER" or ACQ_TYPE == "AVERage": becasue the scope ALWAYS returns the short form
        POINTS_MODE = "NORMal" # Use for Average and High Resoultion acquisition Types.
    else:
        POINTS_MODE = "RAW" # Use for Acq. Type NORMal or PEAK
    
    MSOX4024A.write(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON))
    MSOX4024A.write(":WAVeform:POINts MAX") # This command sets the points mode to MAX AND ensures that the maximum # of points to be transferred is set, though they must still be on screen
    MSOX4024A.write(":WAVeform:POINts:MODE " + str(POINTS_MODE))
    MAX_CURRENTLY_AVAILABLE_POINTS = int(MSOX4024A.query(":WAVeform:POINts?")) # This is the max number of points currently available - this is for on screen data only - Will not change channel to channel.
    
    ## The scope will return a -222,"Data out of range" error if fewer than 100 points are requested, even though it may actually return fewer than 100 points.
    if USER_REQUESTED_POINTS < 100:
        USER_REQUESTED_POINTS = 100
    
    if MAX_CURRENTLY_AVAILABLE_POINTS < 100:
        MAX_CURRENTLY_AVAILABLE_POINTS = 100
    
    if USER_REQUESTED_POINTS > MAX_CURRENTLY_AVAILABLE_POINTS or ACQ_TYPE == "PEAK":
         USER_REQUESTED_POINTS = MAX_CURRENTLY_AVAILABLE_POINTS
    
    ## Tell it how many points you want
    MSOX4024A.write(":WAVeform:POINts " + str(USER_REQUESTED_POINTS))
    
    ## Then ask how many points it will actually give you, as it may not give you exactly what you want.
    NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE = int(MSOX4024A.query(":WAVeform:POINts?"))
    
    Pre = MSOX4024A.query(":WAVeform:PREamble?").split(',') # This does need to be set to a channel that is on, but that is already done... e.g. Pre = MSOX4024A.query(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON) + ";PREamble?").split(',')
    ## While these values can always be used for all analog channels, they need to be retrieved and used separately for math/other waveforms as they will likely be different.
    #ACQ_TYPE    = float(Pre[1]) # Gives the scope Acquisition Type; this is already done above in this particular script
    X_INCrement = float(Pre[4]) # Time difference between data points; Could also be found with :WAVeform:XINCrement? after setting :WAVeform:SOURce
    X_ORIGin    = float(Pre[5]) # Always the first data point in memory; Could also be found with :WAVeform:XORigin? after setting :WAVeform:SOURce
    X_REFerence = float(Pre[6]) # Specifies the data point associated with x-origin; The x-reference point is the first point displayed and XREFerence is always 0.; Could also be found with :WAVeform:XREFerence? after setting :WAVeform:SOURce
    ## This could have been pulled earlier...
    del Pre
    
    DataTime = ((np.linspace(0,NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE-1,NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE)-X_REFerence)*X_INCrement)+X_ORIGin
    if ACQ_TYPE == "PEAK": # This means Peak Detect Acq. Type
        DataTime = np.repeat(DataTime,2)
    
    ## Determine number of bytes that will actually be transferred and set the "chunk size" accordingly.
    ## Get the waveform format
    WFORM = str(MSOX4024A.query(":WAVeform:FORMat?"))
    if WFORM == "BYTE":
        FORMAT_MULTIPLIER = 1
    else: #WFORM == "WORD"
        FORMAT_MULTIPLIER = 2
    
    if ACQ_TYPE == "PEAK":
        POINTS_MULTIPLIER = 2 # Recall that Peak Acq. Type basically doubles the number of points.
    else:
        POINTS_MULTIPLIER = 1
    
    TOTAL_BYTES_TO_XFER = POINTS_MULTIPLIER * NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE * FORMAT_MULTIPLIER + 11
        ## Why + 11?  The IEEE488.2 waveform header for definite length binary blocks (what this will use) consists of 10 bytes.  The default termination character, \n, takes up another byte.
            ## If you are using mutliplr termination characters, adjust accordingly.
        ## Note that Python 2.7 uses ASCII, where all characters are 1 byte.  Python 3.5 uses Unicode, which does not have a set number of bytes per character.
    
    ## Set chunk size:
        ## More info @ http://pyvisa.readthedocs.io/en/stable/resources.html
    if TOTAL_BYTES_TO_XFER >= 400000:
        MSOX4024A.chunk_size = TOTAL_BYTES_TO_XFER
    
    #####################################################
    ## Pull waveform data, scale it
    ## Channel 1
    ## If on, pull data
    if CHAN1_STATE == 1:
        Data_Ch1 = np.array(MSOX4024A.query_binary_values(':WAVeform:SOURce CHANnel1;DATA?', "h", False))
        Data_Ch1 = ((Data_Ch1-Y_REFerence_Ch1)*Y_INCrement_Ch1)+Y_ORIGin_Ch1
    ## Channel 2
    ## If on, pull data
    if CHAN2_STATE == 1:
        Data_Ch2 = np.array(MSOX4024A.query_binary_values(':WAVeform:SOURce CHANnel2;DATA?', "h", False))
        Data_Ch2 = ((Data_Ch2-Y_REFerence_Ch2)*Y_INCrement_Ch2)+Y_ORIGin_Ch2
  ## Channel 3
    ## If on, pull data
    if CHAN3_STATE == 1:
        Data_Ch3 = np.array(MSOX4024A.query_binary_values(':WAVeform:SOURce CHANnel3;DATA?', "h", False))
        Data_Ch3 = ((Data_Ch3-Y_REFerence_Ch3)*Y_INCrement_Ch3)+Y_ORIGin_Ch3                   
   ## Channel 4
    ## If on, pull data
    if CHAN4_STATE == 1:
        Data_Ch4 = np.array(MSOX4024A.query_binary_values(':WAVeform:SOURce CHANnel4;DATA?', "h", False))
        Data_Ch4 = ((Data_Ch4-Y_REFerence_Ch4)*Y_INCrement_Ch4)+Y_ORIGin_Ch4
                   
    ## Reset the chunk size back to default if needed.
    if TOTAL_BYTES_TO_XFER >= 400000:
        MSOX4024A.chunk_size = 20480
    
    MSOX4024A.clear()
    ################################################################################################
        #create saving folder
    timeF = time.strftime("%d_%m_%y")
    CurrFolder = saveDir + "/OsziData_" + timeF
    if not os.path.exists(CurrFolder):
        os.makedirs(CurrFolder)
        
    ## Channel 1
    if CHAN1_STATE == 1:

        filename = CurrFolder + '/' + "_Channel1.npy"
        with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
            np.save(filehandle, np.vstack((DataTime,Data_Ch1)).T) # See comment above regarding np.vstack and .T
        
        ## Read the NUMPY BINARY data back into python with:
        with open(filename, 'rb') as filehandle: # rb means open for reading binary
            recalled_brute_force_NPY_ch1 = np.load(filehandle)
        
        os.remove(filename)
        del filename, filehandle

        # write it to file counter screenshot index
        for i in range(0,50):
            ChDataFilePath = CurrFolder + '/' + "Ch1Data_%d.dat" %i
            if not os.path.exists(ChDataFilePath):
                np.savetxt(ChDataFilePath ,recalled_brute_force_NPY_ch1)
                print('Channel 1 Data saved as:  ' + "Ch1Data_%d.dat" %i)
                break

    
    ## Channel 2
    if CHAN2_STATE == 1:
    
        filename = CurrFolder + '/' + "_Channel2.npy"
        with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
            np.save(filehandle, np.vstack((DataTime,Data_Ch2)).T) # See comment above regarding np.vstack and .T
    
        ## Read the NUMPY BINARY data back into python with:
        with open(filename, 'rb') as filehandle: # rb means open for reading binary
            recalled_brute_force_NPY_ch2 = np.load(filehandle)
            
        os.remove(filename)
        del filename, filehandle

        # write it to file counter screenshot index
        for i in range(0,50):
            ChDataFilePath = CurrFolder + '/' + "Ch2Data_%d.dat" %i
            if not os.path.exists(ChDataFilePath):
                np.savetxt(ChDataFilePath ,recalled_brute_force_NPY_ch2)
                print('Channel 2 Data saved as:  ' + "Ch2Data_%d.dat" %i)
                break

        
    ## Channel 3
    if CHAN3_STATE == 1:
    
        filename = CurrFolder + '/' + "_Channel3.npy"
        with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
            np.save(filehandle, np.vstack((DataTime,Data_Ch3)).T) # See comment above regarding np.vstack and .T
    
        ## Read the NUMPY BINARY data back into python with:
        with open(filename, 'rb') as filehandle: # rb means open for reading binary
            recalled_brute_force_NPY_ch3 = np.load(filehandle)
        
        os.remove(filename)
        del filename, filehandle
        
        # write it to file counter screenshot index
        for i in range(0,50):
            ChDataFilePath = CurrFolder + '/' + "Ch3Data_%d.dat" %i
            if not os.path.exists(ChDataFilePath):
                np.savetxt(ChDataFilePath ,recalled_brute_force_NPY_ch3)
                print('Channel 3 Data saved as:  ' + "Ch3Data_%d.dat" %i)
                break

    ## Channel 4
    if CHAN4_STATE == 1:
            
        filename = CurrFolder + '/' + "_Channel4.npy"
        with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
            np.save(filehandle, np.vstack((DataTime,Data_Ch4)).T) # See comment above regarding np.vstack and .T
    
        ## Read the NUMPY BINARY data back into python with:
        with open(filename, 'rb') as filehandle: # rb means open for reading binary
            recalled_brute_force_NPY_ch4 = np.load(filehandle)
        
        os.remove(filename)
        del filename, filehandle
        
        # write it to file counter screenshot index
        for i in range(0,50):
            ChDataFilePath = CurrFolder + '/' + "Ch4Data_%d.dat" %i
            if not os.path.exists(ChDataFilePath):
                np.savetxt(ChDataFilePath ,recalled_brute_force_NPY_ch4)
                print('Channel 4 Data saved as:  ' + "Ch4Data_%d.dat" %i)
                break
                
    print ('Data of all active channels saved.\n')
    
    
    
    
def Screenshot(saveDir):
        
    # configure ink saver (black background as seen on screen)
    MSOX4024A.write(':HARDcopy:INKSaver 0')
    # get screen data
    data = MSOX4024A.query_binary_values(':DISPlay:DATA? PNG, COLOR', datatype='B')
    
    #create saving folder
    timeF = time.strftime("%d_%m_%y")
    
    if not os.path.exists(saveDir + "/OsziData_" + timeF):
        os.makedirs(saveDir + "/OsziData_" + timeF)
    # write it to file counter screenshot index
    for i in range(0,50):
        ScreenshotFilePath = saveDir + "/OsziData_" + timeF + '/Screenshot%d.png' %i
        if not os.path.exists(ScreenshotFilePath):
            newfile=open(ScreenshotFilePath,'wb')
            newfile.write(bytearray(data))
            newfile.close()
            break
        
    print('Screenshot saved as:  ' + 'Screenshot%d.png' %i)





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
            print('Transfering Screenshot')
            Screenshot(saveDir)
        elif i==5:
            if FileDialogFlag == False:
                FileDialogFlag = True
                saveDir = filedialog.askdirectory()
            print('Transfering Data')
            TransferData(saveDir)
        else:
            print('Button not supported')
            
#def WidenTimeBase():
#   
#    CurrScaleStr = str(MSOX4024A.query(":TIMebase:SCALe?"))
#    CurrScale = float(CurrScaleStr[1:-1])
#    index = TimeBaseLookUp.index(CurrScale)
#
#    index = index + 1
#    MSOX4024A.write(":TIMebase:SCALe " + str(TimeBaseLookUp[index]))

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
            
            print('Use floor switch to control the oscilloscope\n')
            
            while True:
                x = ser.read()
                
                k = str(x)
                
                try:
                    command = int(k[2])
                    
                    if command == 0:
                        print('Run')
                        MSOX4024A.write(":RUN")
                    if command == 1:
                        print('Stop')
                        MSOX4024A.write(":STOP")
                    if command == 2:
                        print('Single')
                        MSOX4024A.write(":SINGle")
                    if command == 3:
                        if FileDialogFlag == False:
                            FileDialogFlag = True
                            saveDir = filedialog.askdirectory()
                        print('Transfering Screenshot')
                        Screenshot(saveDir)
                    if command == 4:
                        if FileDialogFlag == False:
                            FileDialogFlag = True
                            saveDir = filedialog.askdirectory()
                        print('Transfering Data')
                        TransferData(saveDir)
                    if command == 5:
                        AdjustTimeBase('n')
                        print('Narrow Timebase')
                    if command == 6:
                        AdjustTimeBase('w')
                        print('Widen Timebase')
    
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
root = tk.Tk()
root.withdraw()   
#VISA-Ressource
GLOBAL_TOUT =  20000     
SCOPE_VISA_ADDRESS = "USB0::0x0957::0x17B6::MY56310539::0::INSTR" 
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') 

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
#print("ready\n")
mode = 'f' #input('Press -k- for Keyboard operation or -f- for floor switch')

if mode == 'k':
    print("Press:")
    print("4 -> Run")
    print("1 -> Stop")
    print("3 -> Single")
    print("2 -> Transfer Screenshot to PC")
    print("5 -> Transfer Data to PC")
    Control()
elif mode == 'f':
    ControlSerial()
else:
    print('\n--not a valid mode--\n Aborting Script...')
    time.sleep(5)
    sys.exit()

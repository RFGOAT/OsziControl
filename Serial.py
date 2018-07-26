#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:26:31 2017

@author: achim
"""

import serial

#def ReadUSB():
#    USBData = ser.readline()
#    time.sleep(1)
#    return USBData

with serial.Serial('COM12', 9600, timeout=1) as ser:

    while True:
        x = ser.read()
        
        k = str(x)
        
        try:
            command = int(k[2])
            
            print(command)

        except Exception:
            i = k # Dummy
            
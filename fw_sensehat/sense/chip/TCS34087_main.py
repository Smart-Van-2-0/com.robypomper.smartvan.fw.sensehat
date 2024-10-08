#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import time
try:
    import RPi.GPIO as GPIO
    _gpio_loaded = True
except:
    print("WARN: RPi.GPIO module disabled.")
    _gpio_loaded = False
from TCS34087 import TCS34087

try:
    Light=TCS34087(0X29, debug=False)
    if(Light.TCS34087_init() == 1):
        print("TCS34087 initialization error!!")
    else:
        print("TCS34087 initialization success!!")
    # time.sleep(2)
    while True:
        Light.Get_RGBData()
        Light.GetRGB888()
        Light.GetRGB565()
        print("R: %d "%Light.RGB888_R, end = "")
        print("G: %d "%Light.RGB888_G, end = "")
        print("B: %d "%Light.RGB888_B, end = "") 
        print("C: %#x "%Light.C, end = "")
        print("RGB565: %#x "%Light.RGB565, end ="")
        print("RGB888: %#x "%Light.RGB888, end = "")   
        print("LUX: %d "%Light.Get_Lux(), end = "") 
        print("CT: %dK "%Light.Get_ColorTemp(), end ="")
        print("INT: %d "%Light.GetLux_Interrupt())

except:
    if _gpio_loaded:
        GPIO.cleanup()
    print ("\nProgram end")
    exit()

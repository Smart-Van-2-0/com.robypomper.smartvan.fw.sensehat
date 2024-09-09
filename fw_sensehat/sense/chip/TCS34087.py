#!/usr/bin/python
# coding=utf-8
import time
import smbus

try:
    import RPi.GPIO as GPIO

    _gpio_loaded = True
except:
    print("WARN: RPi.GPIO module disabled.")
    _gpio_loaded = False

# i2c address
I2C_ADD_TCS34087 = 0x29

# GPIO
INT_PORT = 26

TCS34087_R_Coef = 0.136
TCS34087_G_Coef = 1.000
TCS34087_B_Coef = -0.444
TCS34087_GA = 1.0
TCS34087_DF = 310.0
TCS34087_CT_Coef = 3810.0
TCS34087_CT_Offset = 1391.0

TCS34087_G_Offset = 0.92
TCS34087_B_Offset = 0.73

TCS34087_ENABLE = 0x80
# Flicker Detection Enable -  Writing a 1 activates flicker detection
TCS34087_ENABLE_FDEN = 0x40
# Wait enable - Writing 1 activates the wait timer
TCS34087_ENABLE_WEN = 0x08
# ALS Enable - Writing a 1 enables ALS/Color
TCS34087_ENABLE_AEN = 0x02
# Power ON. When asserted, the internal oscillator is activated, allowing timers
# and ADC channels to operate. Only set this bit after all other registers have
# been initialized by the host.
TCS34087_ENABLE_PON = 0x01
# ALS integration time
TCS34087_ATIME = 0x81
# ATIME = ASTEP
TCS34087_ATIME_Time0 = 0x00
# ATIME = ASTEP × (n+1)  n=5
TCS34087_ATIME_Time5 = 0x00
# ATIME = ASTEP × (n+1)  n=65
TCS34087_ATIME_Time41 = 0x41
# ATIME = 256 × ASTEP
TCS34087_ATIME_TimeFF = 0xFF

# ALS Integration Time Step Size
TCS34087_ASTEP = 0x82

# Wait time (if TCS34087_ENABLE_WEN is asserted)
TCS34087_WTIME = 0x83

# ALS interrupt low threshold
TCS34087_AILTL = 0x84
TCS34087_AILTH = 0x85
# ALS interrupt high threshold
TCS34087_AIHTL = 0x86
TCS34087_AIHTH = 0x87

# Auxiliary identification 0x4A
TCS34087_AUXID = 0x90
# Revision identification 0X53
TCS34087_REVID = 0x91
# Device identification 0x18 = TCS34087
TCS34087_ID = 0x92

# Device status one
TCS34087_STATUS = 0x93
# ALS and Flicker Detect Saturation
TCS34087_STATUS_ASAT = 0x80
# ALS Interrupt
TCS34087_STATUS_AINT = 0x04
# Calibration Interrupt
TCS34087_STATUS_CINT = 0x02
# System Interrupt
TCS34087_STATUS_SINT = 0x01

# ALS status
TCS34087_ASTATUS = 0x94
# ALS Saturation Status
TCS34087_ASTATUS_ASAT_STATUS = 0x80
# ALS Gain Status
TCS34087_ASTATUS_AGAIN_STATUS = 0x00

# ALS channel zero data Clear
TCS34087_ADATA0L = 0x95
TCS34087_ADATA0H = 0x96

# ALS channel one data Red
TCS34087_ADATA1L = 0x97
TCS34087_ADATA1H = 0x98

# ALS channel two data Green
TCS34087_ADATA2L = 0x99
TCS34087_ADATA2H = 0x9A

# ALS channel three data Blue
TCS34087_ADATA3L = 0x9B
TCS34087_ADATA3H = 0x9C

# ALS channel four data WIDEBAND data
TCS34087_ADATA4L = 0x9D
TCS34087_ADATA4H = 0x9E

# ALS channel five data  FLICKER data
TCS34087_ADATA5L = 0x9F
TCS34087_ADATA5H = 0xA0

# Device status two
TCS34087_STATUS2 = 0xA3
# ALS Valid
TCS34087_AVALID = 0x40
# ALS Digital Saturation
TCS34087_ASAT_DIGITAL = 0x10
# ALS Analog Saturation
TCS34087_ASAT_ANALOG = 0x80
# Flicker Detect Analog Saturation
TCS34087_FDSAT_ANALOG = 0x02
# Flicker Detect Digital Saturation
TCS34087_FDSAT_DIGITAL = 0x01

# Device status three
TCS34087_STATUS3 = 0xA4
# ALS Interrupt High 
TCS34087_STATUS3_AINT_AIHT = 0x20
# ALS Interrupt Low 
TCS34087_STATUS3_AINT_AILT = 0x10

# Device status five
TCS34087_STATUS5 = 0xA6
# Flicker Detect Interrupt
TCS34087_STATUS5_SINT_FD = 0x08

# Device status six
TCS34087_STATUS6 = 0xA7
# Over Temperature Detected
TCS34087_STATUS6_OVTEMP_DETECTED = 0x20
# Flicker Detect Trigger Error
TCS34087_STATUS6_FD_TRIGGER_ERROR = 0x10
# ALS Trigger Error
TCS34087_STATUS6_ALS_TRIGGER_ERROR = 0x04
# Sleep After Interrupt Active
TCS34087_STATUS6_SAI_ACTIVE = 0x02
# Initialization Busy
TCS34087_STATUS6_INIT_BUSY = 0x01

# Configuration zero
TCS34087_CFG0 = 0xA9
# Low Power Idle
TCS34087_CFG0_LOWPOWER_IDLE = 0x40
# ALS Trigger Long
TCS34087_CFG0_ALS_TRIGGER_LONG = 0x04
# RAM Bank Selection
TCS34087_CFG0_RAM_BANK = 0x00

# Configuration one
TCS34087_CFG1 = 0xAA
# ALS Gain. Sets the ALS sensitivity.
TCS34087_CFG1_AGAIN = 0x09
# Value = 0x00~0x0C Value = 0x00 GAIN = 0.5x GAIN = 2^(Value-1)

# Configuration three
TCS34087_CFG3 = 0xAC
# Sleep After Interrupt
TCS34087_CFG3_SAI = 0x10

# Configuration four
TCS34087_CFG4 = 0xAD
# Interrupt Pin Map
TCS34087_CFG4_INT_PINMAP = 0x40
# Interrupt Invert
TCS34087_CFG4_INT_INVERT = 0x08

# Configuration six
TCS34087_CFG6 = 0xAF
# Figure 35
TCS34087_CFG6_ALS_AGC_MAX_GAIN_START = 0x40

# Configuration eight
TCS34087_CFG8 = 0xB1
# ALS AGC Enable
TCS34087_CFG8_ALS_AGC_ENABLE = 0x04

# Configuration nine
TCS34087_CFG9 = 0xB2
# System Interrupt Flicker Detection
TCS34087_CFG9_SIEN_FD = 0x40

# Configuration ten
TCS34087_CFG10 = 0xB3
# ALS AGC High Hysteresis
TCS34087_CFG10_ALS_AGC_HIGH_HYST = 0xC0
# ALS AGC Low Hysteresis
TCS34087_CFG10_ALS_AGC_LOW_HYST = 0x30
# Flicker Detect Persistence
TCS34087_CFG10_FD_PERS = 0x02

# Configuration eleven
TCS34087_CFG11 = 0xB4
# ALS Interrupt Direct
TCS34087_CFG11_AINT_DIRECT = 0x80

# Configuration twelve
TCS34087_CFG12 = 0xB5
# ALS Thresholds Channel
TCS34087_CFG12_ALS_TH_CHANNEL = 0x00

# Persistence register - basic SW filtering mechanism for interrupts
TCS34087_PERS = 0xBD
# Every RGBC cycle generates an interrupt
TCS34087_PERS_NONE = 0x00
# 1 clean channel value outside threshold range generates an interrupt
TCS34087_PERS_1_CYCLE = 0x01
# 2 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_2_CYCLE = 0x02
# 3 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_3_CYCLE = 0x03
# 5 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_5_CYCLE = 0x04
# 10 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_10_CYCLE = 0x05
# 15 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_15_CYCLE = 0x06
# 20 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_20_CYCLE = 0x07
# 25 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_25_CYCLE = 0x08
# 30 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_30_CYCLE = 0x09
# 35 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_35_CYCLE = 0x0A
# 40 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_40_CYCLE = 0x0B
# 45 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_45_CYCLE = 0x0C
# 50 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_50_CYCLE = 0x0D
# 55 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_55_CYCLE = 0x0E
# 60 clean channel values outside threshold range generates an interrupt
TCS34087_PERS_60_CYCLE = 0x0F

# ALS integration step size
TCS34087_ASTEPL = 0xCA
TCS34087_ASTEPH = 0xCB

# Maximum AGC gains
TCS34087_AGC_GAIN_MAX = 0xCF
# Flicker Detection AGC Gain Max
TCS34087_AGC_GAIN_MAX_AGC_FD_GAIN_MAX = 0x90
# ALS AGC Gain Max
TCS34087_AGC_GAIN_MAX_AGC_AGAIN_MAX = 0x09

# Autozero configuration
TCS34087_AZ_CONFIG = 0xD6
# ALS Autozero Frequency
TCS34087_AZ_CONFIG_AZ_NTH_ITERATION = 0xFF

# Flicker detection configuration zero
TCS34087_FD_STATUS = 0xDB
# Flicker Detection Measurement Valid
TCS34087_FD_STATUS_FD_MEASUREMENT_VALID = 0x20
# Flicker Saturation Detected 
TCS34087_FD_STATUS_FD_SATURATION_DETECTED = 0x10
# Flicker Detection 120Hz Flicker Valid 
TCS34087_FD_STATUS_FD_120HZ_FLICKER_VALID = 0x08
# Flicker Detection 100Hz Flicker Valid 
TCS34087_FD_STATUS_FD_100HZ_FLICKER_VALID = 0x04
# Flicker Detected at 120Hz
TCS34087_FD_STATUS_FD_120HZ_FLICKER = 0x02
# Flicker Detected at 100Hz
TCS34087_FD_STATUS_FD_100HZ_FLICKER = 0x01

# Enable interrupts
TCS34087_INTENAB = 0xF9
# ALS and Flicker Detect Saturation Interrupt Enable
TCS34087_INTENAB_ASIEN = 0x80
# ALS Interrupt Enable
TCS34087_INTENAB_AIEN = 0x04
# System Interrupt Enable
TCS34087_INTENAB_SIEN = 0x01

# Control
TCS34087_CONTROL = 0xFA
# ALS Manual Autozero
TCS34087_CONTROL_ALS_MANUAL_AZ = 0x04
# Clear Sleep-After-Interrupt Active
TCS34087_CONTROL_CLEAR_SAI_ACTIVE = 0x01

# Lum
# Clear channel < 30000
LUM_0 = 36
# Clear channel < 40000
LUM_1 = 48
# Clear channel < 50000
LUM_2 = 65
# Clear channel < 60000
LUM_3 = 80
# Clear channel < 65535
LUM_4 = 104

# Integration Time
# STEP SIZE = 2.78us  VALUE = 0
TCS34725_INTEGRATIONTIME_2_78US = 0x00
# STEP SIZE = 2.78us x (n+1)  VALUE = n
TCS34725_INTEGRATIONTIME_nMS = 0x01
# STEP SIZE = 1.67ms    VALUE = 599
TCS34725_INTEGRATIONTIME_1_67MS = 0x02
# STEP SIZE = 2.78ms   VALUE = 999
TCS34725_INTEGRATIONTIME_2_78MS = 0x03
# STEP SIZE = 50ms   VALUE = 17999
TCS34725_INTEGRATIONTIME_50MS = 0x04
# STEP SIZE = 182ms   VALUE = 65535
TCS34725_INTEGRATIONTIME_182MS = 0x05

# Gain
# 0.5x gain
TCS34087_GAIN_0_5X = 0x00
# No gain
TCS34087_GAIN_1X = 0x01
# 4x gain
TCS34087_GAIN_4X = 0x03
# 8x gain
TCS34087_GAIN_8X = 0x04
# 16x gain
TCS34087_GAIN_16X = 0x05
# 64x gain
TCS34087_GAIN_64X = 0x07
# 128x gain
TCS34087_GAIN_128X = 0x08
# 256x gain
TCS34087_GAIN_256X = 0x09
# 512x gain
TCS34087_GAIN_512X = 0x0A
# 1024x gain
TCS34087_GAIN_1024X = 0x0B
# 2048x gain
TCS34087_GAIN_2048X = 0x0C


class TCS34087:
    gain_t = 0
    integration_time_t = 0
    a_time = 0
    rgb_offset_C = 0
    C = 0
    R = 0
    G = 0
    B = 0
    W = 0
    F = 0
    RGB888 = 0
    RGB888_R = 0
    RGB888_G = 0
    RGB888_B = 0
    RGB565 = 0
    RGB565_R = 0
    RGB565_G = 0
    RGB565_B = 0

    def __init__(self, address=0x29, debug=False):
        self.i2c = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        # Set GPIO mode
        if _gpio_loaded:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(INT_PORT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if self.debug:
            print("Resetting TCS34087")

    def Write_Byte(self, reg, value):
        # "Writes an 8-bit value to the specified register/address"
        self.i2c.write_byte_data(self.address, reg, value)
        if self.debug:
            print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))

    def Write_Word(self, reg, value):
        # "Writes an 16-bit value to the specified register/address"
        self.i2c.write_word_data(self.address, reg, value)
        if self.debug:
            print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))

    def Read_Byte(self, reg):
        # "Read an unsigned byte from the I2C device"
        result = self.i2c.read_byte_data(self.address, reg)
        if self.debug:
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (
                self.address, result & 0xFF, reg))
        return result

    def Read_Word(self, reg):
        # "Read an unsigned byte from the I2C device"
        result = self.i2c.read_word_data(self.address, reg)
        if self.debug:
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (
                self.address, result & 0xFF, reg))
        return result

    def Set_Gain(self, gain):
        self.Write_Byte(TCS34087_CFG1, gain)
        self.gain_t = gain

    def Set_Integration_Time(self, at, t):
        self.Write_Byte(TCS34087_ATIME, at)
        # Update the timing register 
        self.Write_Word(TCS34087_ASTEP, 0xE700 | t)
        self.a_time = at
        self.integration_time_t = t

    def Enable(self):
        self.Write_Byte(TCS34087_ENABLE,
                        TCS34087_ENABLE_FDEN | TCS34087_ENABLE_PON |
                        TCS34087_ENABLE_AEN)
        time.sleep(0.01)

    def Disable(self):
        # Turn the device off to save power
        reg = self.Read_Byte(TCS34087_ENABLE)
        self.Write_Byte(TCS34087_ENABLE, reg & ~(
                TCS34087_ENABLE_FDEN | TCS34087_ENABLE_PON |
                TCS34087_ENABLE_AEN))

    def Interrupt_Enable(self):
        reg = self.Read_Byte(TCS34087_ENABLE)
        self.Write_Byte(TCS34087_ENABLE, reg | TCS34087_INTENAB_AIEN)

    def Interrupt_Disable(self):
        reg = self.Read_Byte(TCS34087_ENABLE)
        self.Write_Byte(TCS34087_ENABLE,
                        reg & (~TCS34087_INTENAB_AIEN))

    def Set_Interrupt_Persistence_Reg(self, per):
        if per < 0x10:
            self.Write_Byte(TCS34087_PERS, per)
        else:
            self.Write_Byte(TCS34087_PERS, TCS34087_PERS_60_CYCLE)

    def Set_Interrupt_Threshold(self, threshold_h, threshold_l):
        self.Write_Byte(TCS34087_AILTL, threshold_l & 0xff)
        self.Write_Byte(TCS34087_AILTH, threshold_l >> 8)
        self.Write_Byte(TCS34087_AIHTL, threshold_h & 0xff)
        self.Write_Byte(TCS34087_AIHTH, threshold_h >> 8)

    def Clear_Interrupt_Flag(self):
        self.Write_Byte(TCS34087_STATUS, TCS34087_STATUS_ASAT)

    def TCS34087_init(self):
        id_read = self.Read_Byte(TCS34087_ID)
        if id_read != 0x18:
            return 1
        self.Set_Integration_Time(TCS34087_ATIME_Time41,
                                  TCS34725_INTEGRATIONTIME_2_78MS)
        self.Set_Gain(TCS34087_GAIN_128X)
        self.integration_time_t = TCS34725_INTEGRATIONTIME_2_78MS
        self.gain_t = TCS34087_GAIN_128X
        self.Enable()
        self.Interrupt_Enable()
        self.Set_Interrupt_Threshold(0xff00, 0x00ff)
        self.Set_Interrupt_Persistence_Reg(TCS34087_PERS_2_CYCLE)
        self.rgb_offset_C = LUM_1
        return 0

    def GetLux_Interrupt(self):
        if _gpio_loaded:
            if GPIO.input(INT_PORT) == GPIO.LOW:
                self.Clear_Interrupt_Flag()
                return 1

        return 0

    def Read_ID(self):
        return self.Read_Byte(TCS34087_ID)

    def Get_RGBData(self):
        self.C = self.Read_Word(TCS34087_ADATA0L)
        self.R = self.Read_Word(TCS34087_ADATA1L)
        self.G = self.Read_Word(TCS34087_ADATA2L)
        self.B = self.Read_Word(TCS34087_ADATA3L)
        self.W = self.Read_Word(TCS34087_ADATA4L)
        self.F = self.Read_Word(TCS34087_ADATA5L)

        if self.integration_time_t == TCS34725_INTEGRATIONTIME_2_78US:
            # time.sleep(0.01)
            pass
        elif self.integration_time_t == TCS34725_INTEGRATIONTIME_nMS:
            time.sleep(0.00278 * (self.a_time + 1))
        elif self.integration_time_t == TCS34725_INTEGRATIONTIME_1_67MS:
            time.sleep(0.016)
        elif self.integration_time_t == TCS34725_INTEGRATIONTIME_2_78MS:
            time.sleep(0.03)
        elif self.integration_time_t == TCS34725_INTEGRATIONTIME_50MS:
            time.sleep(0.05)
        elif self.integration_time_t == TCS34725_INTEGRATIONTIME_182MS:
            time.sleep(0.18)

    def GetRGB888(self):
        """ Convert read data to RGB888 format """

        if self.rgb_offset_C != 0:
            self.RGB888_R = self.R // self.rgb_offset_C
            self.RGB888_G = self.G // self.rgb_offset_C // TCS34087_G_Offset
            self.RGB888_B = self.B // self.rgb_offset_C // TCS34087_B_Offset

        if self.RGB888_R > 30:
            self.RGB888_R = self.RGB888_R - 30
        if self.RGB888_G > 30:
            self.RGB888_G = self.RGB888_G - 30
        if self.RGB888_B > 30:
            self.RGB888_B = self.RGB888_B - 30

        self.RGB888_R = int(self.RGB888_R * 255 // 225)
        self.RGB888_G = int(self.RGB888_G * 255 // 225)
        self.RGB888_B = int(self.RGB888_B * 255 // 225)

        if self.RGB888_R > 255:
            self.RGB888_R = 255
        if self.RGB888_G > 255:
            self.RGB888_G = 255
        if self.RGB888_B > 255:
            self.RGB888_B = 255

        self.RGB888 = (self.RGB888_R << 16) | (self.RGB888_G << 8) | (
            self.RGB888_B)

    def GetRGB565(self):
        """ Convert read data to RGB565 format """

        if self.rgb_offset_C != 0:
            self.RGB565_R = self.R // self.rgb_offset_C
            self.RGB565_G = self.G // self.rgb_offset_C // TCS34087_G_Offset
            self.RGB565_B = self.B // self.rgb_offset_C // TCS34087_B_Offset

        if self.RGB565_R > 30:
            self.RGB565_R = self.RGB565_R - 30
        if self.RGB565_G > 30:
            self.RGB565_G = self.RGB565_G - 30
        if self.RGB565_B > 30:
            self.RGB565_B = self.RGB565_B - 30

        self.RGB565_R = int(self.RGB565_R * 255 // 225)
        self.RGB565_G = int(self.RGB565_G * 255 // 225)
        self.RGB565_B = int(self.RGB565_B * 255 // 225)

        if self.RGB565_R > 255:
            self.RGB565_R = 255
        if self.RGB565_G > 255:
            self.RGB565_G = 255
        if self.RGB565_B > 255:
            self.RGB565_B = 255

        self.RGB565 = (((self.RGB565_R >> 3) << 11) | (
                (self.RGB565_G >> 2) << 5) | (self.RGB565_B >> 3)) & 0xffff

    def Get_Lux(self):
        """
        The Get_Lux function calculates and returns the illuminance in lux based
        on the RGB readings from a TCS34087 color sensor. The function utilizes
        the integration time, gain, and color coefficients to perform the
        necessary computations.

        :return: Calculated illuminance in lux
        """

        atime_ms = ((256 - self.integration_time_t) * 2.4)
        if self.R + self.G + self.B > self.C:
            ir = (self.R + self.G + self.B - self.C) / 2
        else:
            ir = 0
        r_comp = self.R - ir
        g_comp = self.G - ir
        b_comp = self.B - ir
        gain_temp = 1
        if self.gain_t == TCS34087_GAIN_0_5X:
            gain_temp = 0.5
        elif self.gain_t == TCS34087_GAIN_1X:
            gain_temp = 1
        elif self.gain_t == TCS34087_GAIN_4X:
            gain_temp = 4
        elif self.gain_t == TCS34087_GAIN_8X:
            gain_temp = 8
        elif self.gain_t == TCS34087_GAIN_16X:
            gain_temp = 16
        elif self.gain_t == TCS34087_GAIN_64X:
            gain_temp = 64
        elif self.gain_t == TCS34087_GAIN_128X:
            gain_temp = 128
        elif self.gain_t == TCS34087_GAIN_256X:
            gain_temp = 256
        elif self.gain_t == TCS34087_GAIN_512X:
            gain_temp = 512
        elif self.gain_t == TCS34087_GAIN_1024X:
            gain_temp = 1024
        elif self.gain_t == TCS34087_GAIN_2048X:
            gain_temp = 2048

        cpl = (atime_ms * gain_temp) / (TCS34087_GA * TCS34087_DF)
        lux = (TCS34087_R_Coef * float(r_comp) + TCS34087_G_Coef *
               float(g_comp) + TCS34087_B_Coef * float(b_comp)) / cpl
        return lux

    def Get_ColorTemp(self):
        ir = 0
        if self.R + self.G + self.B > self.C:
            ir = (self.R + self.G + self.B - self.C - 1) / 2
        r_comp = self.R - ir
        b_comp = self.B - ir
        try:
            cct = (TCS34087_CT_Coef * float(b_comp) /
                   float(r_comp) + TCS34087_CT_Offset)
        except ZeroDivisionError:
            return 0.0
        return cct

    def readAll(self):
        self.Get_RGBData()
        self.GetRGB888()
        self.GetRGB565()

    def get_last_rgb(self) -> (int, int, int):
        return self.RGB888_R, self.RGB888_G, self.RGB888_B

    def get_last_clear(self) -> int:
        return self.C

    def get_last_rgb565(self) -> int:
        return self.RGB565

    def get_last_rgb888(self) -> int:
        return self.RGB888

    def get_last_lux(self) -> int:
        return self.Get_Lux()

    def get_last_lux_interrupt(self) -> int:
        return self.GetLux_Interrupt()

    def get_last_color_temp(self) -> float:
        return round(self.Get_ColorTemp(), 2)
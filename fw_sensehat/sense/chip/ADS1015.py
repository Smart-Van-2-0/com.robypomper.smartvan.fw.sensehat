#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import smbus

# i2c address
I2C_ADD_ADS1015 = 0x48

# Pointer Register
ADS_POINTER_CONVERT = 0x00
ADS_POINTER_CONFIG = 0x01
ADS_POINTER_LOW_THRESHOLD = 0x02
ADS_POINTER_HIGH_THRESHOLD = 0x03

# Config Register
# Device is currently performing a conversion
ADS_CONFIG_OS_BUSY = 0x0000
# Device is not currently performing a conversion              
ADS_CONFIG_OS_NO_BUSY = 0x8000
# Start a single conversion (when in power-down state)  
ADS_CONFIG_OS_SINGLE_CONVERT = 0x8000
# No effect
ADS_CONFIG_OS_NO_EFFECT = 0x0000
# Input multiplexer, AINP = AIN0 and AINN = AIN1(default)
ADS_CONFIG_MUX_MUL_0_1 = 0x0000
# Input multiplexer, AINP = AIN0 and AINN = AIN3
ADS_CONFIG_MUX_MUL_0_3 = 0x1000
# Input multiplexer, AINP = AIN1 and AINN = AIN3
ADS_CONFIG_MUX_MUL_1_3 = 0x2000
# Input multiplexer, AINP = AIN2 and AINN = AIN3
ADS_CONFIG_MUX_MUL_2_3 = 0x3000
# SINGLE,AIN0
ADS_CONFIG_MUX_SINGLE_0 = 0x4000
# SINGLE,AIN1
ADS_CONFIG_MUX_SINGLE_1 = 0x5000
# SINGLE,AIN2
ADS_CONFIG_MUX_SINGLE_2 = 0x6000
# SINGLE,AIN3
ADS_CONFIG_MUX_SINGLE_3 = 0x7000
# Gain= +/- 6.144V
ADS_CONFIG_PGA_6144 = 0x0000
# Gain= +/- 4.096V
ADS_CONFIG_PGA_4096 = 0x0200
# Gain= +/- 2.048V(default)
ADS_CONFIG_PGA_2048 = 0x0400
# Gain= +/- 1.024V
ADS_CONFIG_PGA_1024 = 0x0600
# Gain= +/- 0.512V
ADS_CONFIG_PGA_512 = 0x0800
# Gain= +/- 0.256V
ADS_CONFIG_PGA_256 = 0x0A00
# Device operating mode:Continuous-conversion mode        
ADS_CONFIG_MODE_CONTINUOUS = 0x0000
# Device operating mode：Single-shot mode or power-down state (default)
ADS_CONFIG_MODE_NO_CONTINUOUS = 0x0100
# Data rate=7.5Hz
ADS_CONFIG_DR_RATE_7_5 = 0x0000
# Data rate=15Hz
ADS_CONFIG_DR_RATE_15 = 0x0020
# Data rate=30Hz
ADS_CONFIG_DR_RATE_30 = 0x0040
# Data rate=60Hz
ADS_CONFIG_DR_RATE_60 = 0x0060
# Data rate=120Hz
ADS_CONFIG_DR_RATE_120 = 0x0080
# Data rate=240Hz
ADS_CONFIG_DR_RATE_240 = 0x00A0
# Data rate=480Hz
ADS_CONFIG_DR_RATE_480 = 0x00C0
# Data rate=960Hz
ADS_CONFIG_DR_RATE_960 = 0x00E0
# Comparator mode：Window comparator
ADS_CONFIG_COMP_MODE_WINDOW = 0x0010
# Comparator mode：Traditional comparator (default)
ADS_CONFIG_COMP_MODE_TRADITIONAL = 0x0000
# Comparator polarity：Active low (default)
ADS_CONFIG_COMP_POL_LOW = 0x0000
# Comparator polarity：Active high
ADS_CONFIG_COMP_POL_HIGH = 0x0008
# Latching comparator 
ADS_CONFIG_COMP_LAT = 0x0004
# Non latching comparator (default)
ADS_CONFIG_COMP_NON_LAT = 0x0000
# Assert after one conversion
ADS_CONFIG_COMP_QUE_ONE = 0x0000
# Assert after two conversions
ADS_CONFIG_COMP_QUE_TWO = 0x0001
# Assert after four conversions
ADS_CONFIG_COMP_QUE_FOUR = 0x0002
# Disable comparator and set ALERT/RDY pin to high-impedance (default)
ADS_CONFIG_COMP_QUE_NON = 0x0003

Config_Set = 0


class ADS1015(object):
    def __init__(self, address=I2C_ADD_ADS1015):
        self._address = address
        self._bus = smbus.SMBus(1)

        state = self._read_u16(ADS_POINTER_CONFIG) & 0x8000
        if state != 0x8000:
            raise IOError("Can't init ADS1015 via I2C on address '{}'".format(
                self._address))

    def ADS1015_SINGLE_READ(self, channel):
        """ Read single channel data. """
        config_set = (
                # mode：Single-shot mode or power-down state
                ADS_CONFIG_MODE_NO_CONTINUOUS |
                # Gain= +/- 4.096V
                ADS_CONFIG_PGA_4096 |
                # Disable comparator
                ADS_CONFIG_COMP_QUE_NON |
                # Non latching comparator
                ADS_CONFIG_COMP_NON_LAT |
                # Comparator polarity：Active low
                ADS_CONFIG_COMP_POL_LOW |
                # Traditional comparator
                ADS_CONFIG_COMP_MODE_TRADITIONAL |
                # Data rate=480Hz
                ADS_CONFIG_DR_RATE_480
        )
        if channel == 0:
            config_set |= ADS_CONFIG_MUX_SINGLE_0
        elif channel == 1:
            config_set |= ADS_CONFIG_MUX_SINGLE_1
        elif channel == 2:
            config_set |= ADS_CONFIG_MUX_SINGLE_2
        elif channel == 3:
            config_set |= ADS_CONFIG_MUX_SINGLE_3
        config_set |= ADS_CONFIG_OS_SINGLE_CONVERT
        self._write_word(ADS_POINTER_CONFIG, config_set)
        time.sleep(0.02)
        data = self._read_u16(ADS_POINTER_CONVERT)
        return data

    def _read_u16(self, cmd):
        lsb = self._bus.read_byte_data(self._address, cmd)
        msb = self._bus.read_byte_data(self._address, cmd + 1)
        return (lsb << 8) + msb

    def _write_word(self, cmd, val):
        val_h = val & 0xff
        val_l = val >> 8
        val = (val_h << 8) | val_l
        self._bus.write_word_data(self._address, cmd, val)

    def readAll(self) -> (int, int, int, int):
        a0 = self.ADS1015_SINGLE_READ(0)
        a1 = self.ADS1015_SINGLE_READ(1)
        a2 = self.ADS1015_SINGLE_READ(2)
        a3 = self.ADS1015_SINGLE_READ(3)

        return a0, a1, a2, a3


if __name__ == '__main__':

    print("\nADS1015 Test Program ...\r\n")
    ads1015 = ADS1015()

    while True:
        try:
            time.sleep(0.5)
            AIN0_DATA, AIN1_DATA, AIN2_DATA, AIN3_DATA = ads1015.readAll()
            print('\nAIN0 = %d(%.2fmv), AIN1 = %d(%.2fmv), '
                  'AIN2 = %d(%.2fmv), AIN3 = %d(%.2fmv)\n\r' % (
                    AIN0_DATA, AIN0_DATA * 0.125, AIN1_DATA, AIN1_DATA * 0.125,
                    AIN2_DATA, AIN2_DATA * 0.125, AIN3_DATA, AIN3_DATA * 0.125))
        except KeyboardInterrupt:
            print("\n")
            break

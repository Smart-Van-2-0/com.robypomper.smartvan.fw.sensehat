#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import smbus

# i2c address
I2C_ADD_LPS22HB = 0x5C

# Register
LPS_ID = 0xB1
# Interrupt register
LPS_INT_CFG = 0x0B
# Pressure threshold registers
LPS_THS_P_L = 0x0C
LPS_THS_P_H = 0x0D
# Who am I
LPS_WHO_AM_I = 0x0F
# Control registers
LPS_CTRL_REG1 = 0x10
LPS_CTRL_REG2 = 0x11
LPS_CTRL_REG3 = 0x12
# FIFO configuration register
LPS_FIFO_CTRL = 0x14
# Reference pressure registers
LPS_REF_P_XL = 0x15
LPS_REF_P_L = 0x16
LPS_REF_P_H = 0x17
# Pressure offset registers
LPS_RPDS_L = 0x18
LPS_RPDS_H = 0x19
# Resolution register
LPS_RES_CONF = 0x1A
# Interrupt register
LPS_INT_SOURCE = 0x25
# FIFO status register
LPS_FIFO_STATUS = 0x26
# Status register
LPS_STATUS = 0x27
# Pressure output registers
LPS_PRESS_OUT_XL = 0x28
LPS_PRESS_OUT_L = 0x29
LPS_PRESS_OUT_H = 0x2A
# Temperature output registers
LPS_TEMP_OUT_L = 0x2B
LPS_TEMP_OUT_H = 0x2C
# Filter reset register
LPS_RES = 0x33




class LPS22HB(object):
    def __init__(self, address=I2C_ADD_LPS22HB):
        self._address = address
        self._bus = smbus.SMBus(1)

        self.pressure = 0.0
        self.temperature = 0.0

        # Wait for reset to complete
        self.LPS22HB_RESET()
        # Low-pass filter disabled , output registers not updated until MSB and
        # LSB have been read , Enable Block Data Update , Set Output Data Rate
        # to 0
        self._write_byte(LPS_CTRL_REG1, 0x02)

    def LPS22HB_RESET(self):
        buf = self._read_u16(LPS_CTRL_REG2)
        buf |= 0x04
        # SWRESET Set 1
        self._write_byte(LPS_CTRL_REG2, buf)
        while buf:
            buf = self._read_u16(LPS_CTRL_REG2)
            buf &= 0x04

    def LPS22HB_START_ONESHOT(self):
        buf = self._read_u16(LPS_CTRL_REG2)
        buf |= 0x01  # ONE_SHOT Set 1
        self._write_byte(LPS_CTRL_REG2, buf)

    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _read_u16(self, cmd):
        lsb = self._bus.read_byte_data(self._address, cmd)
        msb = self._bus.read_byte_data(self._address, cmd + 1)
        return (msb << 8) + lsb

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)

    def refreshAll(self):
        u8buf = [0, 0, 0]

        self.LPS22HB_START_ONESHOT()
        if (self._read_byte(LPS_STATUS) & 0x01) == 0x01:  # a new pressure data is generated
            u8buf[0] = self._read_byte(LPS_PRESS_OUT_XL)
            u8buf[1] = self._read_byte(LPS_PRESS_OUT_L)
            u8buf[2] = self._read_byte(LPS_PRESS_OUT_H)
            self.pressure = ((u8buf[2] << 16) + (
                    u8buf[1] << 8) + u8buf[0]) / 4096.0
        if (self._read_byte(
                LPS_STATUS) & 0x02) == 0x02:  # a new temperature data is generated
            u8buf[0] = self._read_byte(LPS_TEMP_OUT_L)
            u8buf[1] = self._read_byte(LPS_TEMP_OUT_H)
            self.temperature = ((u8buf[1] << 8) + u8buf[
                0]) / 100.0

    def getPressure(self):
        return round(self.pressure, 2)

    def getTemperature(self):
        return round(self.temperature, 2)


if __name__ == '__main__':
    PRESS_DATA = 0.0
    TEMP_DATA = 0.0
    u8Buf = [0, 0, 0]
    print("\nPressure Sensor Test Program ...\n")
    lps22hb = LPS22HB()
    while True:
        try:
            time.sleep(0.1)
            lps22hb.refreshAll()
            PRESS_DATA = lps22hb.getPressure()
            TEMP_DATA = lps22hb.getTemperature()
            print('Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n' % (
                PRESS_DATA, TEMP_DATA))
        except KeyboardInterrupt:
            print("\n")
            break

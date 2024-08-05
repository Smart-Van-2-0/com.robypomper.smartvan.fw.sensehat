#!/usr/bin/python
# -*- coding:utf-8 -*-
import board
import adafruit_shtc3


class SHTC3(object):

    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self._sht = adafruit_shtc3.SHTC3(i2c)

    def readAll(self):
        return self._sht.temperature, self._sht.relative_humidity

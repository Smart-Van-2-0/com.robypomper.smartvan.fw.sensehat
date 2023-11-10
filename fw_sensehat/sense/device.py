#!/usr/bin/python3
from typing import Optional
import logging

try:
    import RPi.GPIO as GPIO

    _gpio_loaded = True
except:
    print("WARN: RPi.GPIO module disabled.")
    _gpio_loaded = False

from fw_sensehat.sense.mappings import *
from fw_sensehat.device import DeviceAbs
from fw_sensehat.sense.chip.IMU import IMU
from fw_sensehat.sense.chip.LPS22HB import LPS22HB
from fw_sensehat.sense.chip.ADS1015 import ADS1015
# from fw_sensehat.sense.chip.SHTC3 import SHTC3
from fw_sensehat.sense.chip.TCS34087 import TCS34087

logger = logging.getLogger()

from fw_sensehat.sense.chip.IMU import I2C_ADD_IMU_QMI8658
from fw_sensehat.sense.chip.IMU import I2C_ADD_IMU_AK09918
from fw_sensehat.sense.chip.LPS22HB import I2C_ADD_LPS22HB
from fw_sensehat.sense.chip.ADS1015 import I2C_ADD_ADS1015
from fw_sensehat.sense.chip.TCS34087 import I2C_ADD_TCS34087


class Device(DeviceAbs):
    """
    Device class for Sense Hat devices communicating via Serial port
    """

    def __init__(self, auto_refresh=True):
        self._data = {}

        self._is_connected = False
        self._is_reading = False
        self._must_terminate = False

        self.cached_pid = None  # version can be anything else
        self.cached_type = None
        self.cached_type_code = None

        self._imu: Optional[IMU] = None
        self._imu_motion_val = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._lps22hb: Optional[LPS22HB] = None
        self._ads1015: Optional[ADS1015] = None
        self._shtc3 = None
        # self._shtc3 : Optional[SHTC3] = None
        self._tcs34087: Optional[TCS34087] = None
        self.init_chips()

        if auto_refresh:
            self.refresh()

    def __del__(self):
        if _gpio_loaded:
            GPIO.cleanup()

    def init_chips(self):
        try:
            self._imu = IMU(I2C_ADD_IMU_QMI8658, I2C_ADD_IMU_AK09918)
            self._lps22hb = LPS22HB(I2C_ADD_LPS22HB)
            self._ads1015 = ADS1015(I2C_ADD_ADS1015)
            # self._shtc3 = SHTC3()
            self._tcs34087 = TCS34087(I2C_ADD_TCS34087, debug=False)
            if self._tcs34087.TCS34087_init() == 1:
                logger.warning("TCS34087 initialization error!!")
                self._tcs34087 = None
            self._is_connected = True

        except Exception as err:
            self._is_connected = False
            logger.warning(
                "Error on Chips initialization '{}'. Print stacktrace:".format(
                    err))
            import traceback
            traceback.print_exc()
            if _gpio_loaded:
                GPIO.cleanup()

    def refresh(self, reset_data=False):
        """
        Refresh latest data querying them to the device, if `reset_data` is true,
        then default-Zero values are set.
        """

        if not self._is_connected:
            self.init_chips()
            if not self._is_connected:
                return False

        if self._is_reading:
            while self._is_reading or self._must_terminate:
                pass
            if self._must_terminate:
                return False
            return self._is_connected

        self._is_reading = True
        if reset_data:
            self._data = {}
        self._read_data()

        # for k in self._data.keys():
        #    print("'{}': '{}'".format(k, self._data[k]))

        self._is_reading = False
        return self._is_connected

    @property
    def is_connected(self) -> bool:
        """ Returns True if at last refresh attempt the serial device was available. """
        return self._is_connected

    @property
    def is_reading(self) -> bool:
        """ Returns the local device (eg: '/dev/ttyUSB0') used to connect to the serial device """
        return self._is_reading

    def terminate(self):
        """
        Send the terminate signal to all device process and loops.
        """
        self._must_terminate = True

    @property
    def device_pid(self) -> "str | None":
        """
        Returns the device PID, it can be used as index for the PID dict.
        In the Sense Hat case is the hardcoded device's model.
        """

        if self.cached_pid is None:
            self.cached_pid = self._data['hardcoded_model']

        return self.cached_pid

    @property
    def device_type(self) -> str:
        """ Returns the device type """
        if self.cached_type is None:
            if self.device_pid is not None:
                self.cached_type = PID[self.device_pid]['type']

        return self.cached_type \
            if self.cached_type is not None else DEV_TYPE_UNKNOWN

    @property
    def device_type_code(self) -> str:
        """ Returns the device type as a code string"""

        if self.cached_type_code is None and self.device_type is not None:
            self.cached_type_code = dev_type_to_code(self.device_type)

        return self.cached_type_code

    @property
    def latest_data(self) -> dict:
        return self._data

    def _read_data(self):
        """ Read the latest values from sensor's chips. """

        self._data['hardcoded_model'] = "SenseHat(c)"
        try:
            self._read_data_imu()
            self._read_data_lphb()
            self._read_data_ads1015()
            self._read_data_shtc3()
            self._read_data_tcs34087()
        except Exception as err:
            logger.warning(
                "Error during device fetching: [{}] {}".format(type(err),
                                                               str(err)))

    def _read_data_imu(self):
        if self._imu is None:
            logger.debug("IMU not available (Acc, Gyro, Mag...)")
            return

        import math
        # from fw_sensehat.sense.chip.IMU import MotionVal
        # MotionVal = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        MotionVal = self._imu_motion_val
        from fw_sensehat.sense.chip.IMU import Gyro, Accel, Mag
        # Gyro = [0, 0, 0]
        # Accel = [0, 0, 0]
        # Mag = [0, 0, 0]
        from fw_sensehat.sense.chip.IMU import q0, q1, q2, q3
        # q0 = 1.0
        # q1=q2=q3=0.0

        self._imu.QMI8658_Gyro_Accel_Read()
        self._imu.AK09918_MagRead()
        self._imu.icm20948CalAvgValue(MotionVal)
        self._imu.imu_ahrs_update(MotionVal[0] * 0.0175, MotionVal[1] * 0.0175,
                                  MotionVal[2] * 0.0175,
                                  MotionVal[3], MotionVal[4], MotionVal[5],
                                  MotionVal[6], MotionVal[7], MotionVal[8])
        pitch = math.asin(-2 * q1 * q3 + 2 * q0 * q2) * 57.3
        roll = math.atan2(2 * q2 * q3 + 2 * q0 * q1,
                          -2 * q1 * q1 - 2 * q2 * q2 + 1) * 57.3
        yaw = math.atan2(-2 * q1 * q2 - 2 * q0 * q3,
                         2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3

        self._data['imu_roll'] = roll
        self._data['imu_pitch'] = pitch
        self._data['imu_yaw'] = yaw
        self._data['imu_acceleration_x'] = Accel[0]
        self._data['imu_acceleration_y'] = Accel[1]
        self._data['imu_acceleration_z'] = Accel[2]
        self._data['imu_gyroscope_x'] = Gyro[0]
        self._data['imu_gyroscope_y'] = Gyro[1]
        self._data['imu_gyroscope_z'] = Gyro[2]
        self._data['imu_magnetic_x'] = Mag[0]
        self._data['imu_magnetic_y'] = Mag[1]
        self._data['imu_magnetic_z'] = Mag[2]
        self._data['imu_qmi_temperature'] = self._imu.QMI8658_readTemp()

    def _read_data_lphb(self):
        if self._lps22hb is None:
            logger.debug("LPS22HB not available (Press. & Temp.)")
            return

        from fw_sensehat.sense.chip.LPS22HB import LPS_STATUS
        from fw_sensehat.sense.chip.LPS22HB import LPS_PRESS_OUT_XL, \
            LPS_PRESS_OUT_L, LPS_PRESS_OUT_H
        from fw_sensehat.sense.chip.LPS22HB import LPS_TEMP_OUT_L, \
            LPS_TEMP_OUT_H
        u8buf = [0, 0, 0]

        self._lps22hb.LPS22HB_START_ONESHOT()
        if (self._lps22hb._read_byte(
                LPS_STATUS) & 0x01) == 0x01:  # a new pressure data is generated
            u8buf[0] = self._lps22hb._read_byte(LPS_PRESS_OUT_XL)
            u8buf[1] = self._lps22hb._read_byte(LPS_PRESS_OUT_L)
            u8buf[2] = self._lps22hb._read_byte(LPS_PRESS_OUT_H)
            self._data['lps22hb_pressure'] = ((u8buf[2] << 16) + (
                    u8buf[1] << 8) + u8buf[0]) / 4096.0
        if (self._lps22hb._read_byte(
                LPS_STATUS) & 0x02) == 0x02:  # a new temperature data is generated
            u8buf[0] = self._lps22hb._read_byte(LPS_TEMP_OUT_L)
            u8buf[1] = self._lps22hb._read_byte(LPS_TEMP_OUT_H)
            self._data['lps22hb_temperature'] = ((u8buf[1] << 8) + u8buf[
                0]) / 100.0

    def _read_data_ads1015(self):
        if self._ads1015 is None:
            logger.debug("ADS1015 not available (AnalogIn)")
            return

        from fw_sensehat.sense.chip.ADS1015 import ADS_POINTER_CONFIG

        state = self._ads1015._read_u16(ADS_POINTER_CONFIG) & 0x8000
        if state != 0x8000:
            logger.debug("ADS1015 (AnalogIn) Error, state: {}".format(state))
            return

        self._data['ads1015_a0'] = self._ads1015.ADS1015_SINGLE_READ(0)
        self._data['ads1015_a1'] = self._ads1015.ADS1015_SINGLE_READ(1)
        self._data['ads1015_a2'] = self._ads1015.ADS1015_SINGLE_READ(2)
        self._data['ads1015_a3'] = self._ads1015.ADS1015_SINGLE_READ(3)

    def _read_data_shtc3(self):
        if self._shtc3 is None:
            logger.debug("SHTC3 not available (Temp. & Hum.)")
            return

        self._data['shtc3_temperature'] = self._shtc3.SHTC3_Read_Temperature()
        self._data['shtc3_humidity'] = self._shtc3.SHTC3_Read_Humidity()

    def _read_data_tcs34087(self):
        if self._tcs34087 is None:
            logger.debug("TCS34087 (Light sensor)) not available")
            return

        self._tcs34087.Get_RGBData()
        self._tcs34087.GetRGB888()
        self._tcs34087.GetRGB565()

        self._data['tcs34087_rgb_r'] = self._tcs34087.RGB888_R
        self._data['tcs34087_rgb_g'] = self._tcs34087.RGB888_G
        self._data['tcs34087_rgb_b'] = self._tcs34087.RGB888_B
        self._data['tcs34087_c'] = self._tcs34087.C
        self._data['tcs34087_rgb565'] = self._tcs34087.RG565
        self._data['tcs34087_rgb888'] = self._tcs34087.RGB888
        self._data['tcs34087_lux'] = self._tcs34087.Get_Lux()
        self._data['tcs34087_lux_interrupt'] = self._tcs34087.GetLux_Interrupt()
        self._data['tcs34087_color_temp'] = self._tcs34087.Get_ColorTemp()


if __name__ == '__main__':
    v = Device()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))

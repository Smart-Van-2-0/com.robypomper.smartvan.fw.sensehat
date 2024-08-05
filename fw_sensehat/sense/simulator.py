#!/usr/bin/python3

from .device import Device
from .mappings import *
from ..commons import regenerateValue


class DeviceSimulator(Device):

    def __init__(self, auto_refresh = False):
        super().__init__(auto_refresh)
        self._data = {
            'hardcoded_model': 'SenseHat(c)',
            'imu_roll': '0.06830104668952965',
            'imu_pitch': '-25.727970848515366',
            'imu_yaw': '160.75668277388567',
            'imu_acceleration_x': '-1043',
            'imu_acceleration_y': '-1043',
            'imu_acceleration_z': '-1043',
            'imu_gyroscope_x': '1',
            'imu_gyroscope_y': '0',
            'imu_gyroscope_z': '6',
            'imu_magnetic_x': '-267.0',
            'imu_magnetic_y': '57.0',
            'imu_magnetic_z': '-317.0',
            'imu_qmi_temperature': '23.8203125',
            'lps22hb_pressure': '996.468505859375',
            'lps22hb_temperature': '26.15',
            'ads1015_a0': '963',
            'ads1015_a1': '979',
            'ads1015_a2': '995',
            'ads1015_a3': '1011',
            'shtc3_temperature': '23.8203125',
            'shtc3_humidity': '29.8541224',
            'tcs34087_rgb_r': '23',
            'tcs34087_rgb_g': '19',
            'tcs34087_rgb_b': '18',
            'tcs34087_c': '1926',
            'tcs34087_rgb565': '4226',
            'tcs34087_rgb888': '1512210',
            'tcs34087_lux': '1.8633919013504612',
            'tcs34087_lux_interrupt': '0',
            'tcs34087_color_temp': '3083.0112429731416'
        }

    def init_chips(self):
        self._is_connected = True

    def refresh(self, reset_data=False) -> bool:
        self._data = {
            'hardcoded_model': 'SenseHat(c)',
            'imu_roll': regenerateValueMaxMin(self._data['imu_roll'], 0.1, -180, 180),
            'imu_pitch': regenerateValueMaxMin(self._data['imu_pitch'], 0.1, -180, 180),
            'imu_yaw': regenerateValueMaxMin(self._data['imu_yaw'], 0.1, -180, 180),
            'imu_acceleration_x': regenerateValueMaxMin(self._data['imu_acceleration_x'], 0.1, 0, 10),
            'imu_acceleration_y': regenerateValueMaxMin(self._data['imu_acceleration_y'], 0.1, 0, 10),
            'imu_acceleration_z': regenerateValueMaxMin(self._data['imu_acceleration_z'], 0.1, 0, 10),
            'imu_gyroscope_x': regenerateValueMaxMin(self._data['imu_gyroscope_x'], 0.1, 0, 10),
            'imu_gyroscope_y': regenerateValueMaxMin(self._data['imu_gyroscope_y'], 0.1, 0, 10),
            'imu_gyroscope_z': regenerateValueMaxMin(self._data['imu_gyroscope_z'], 0.1, 0, 10),
            'imu_magnetic_x': regenerateValueMaxMin(self._data['imu_magnetic_x'], 0.1, 0, 10),
            'imu_magnetic_y': regenerateValueMaxMin(self._data['imu_magnetic_y'], 0.1, 0, 10),
            'imu_magnetic_z': regenerateValueMaxMin(self._data['imu_magnetic_z'], 0.1, 0, 10),
            'imu_qmi_temperature': regenerateValueMaxMin(self._data['imu_qmi_temperature'], 0.2, -30, 100),
            'lps22hb_pressure': regenerateValueMaxMin(self._data['lps22hb_pressure'], 0.1, 260, 1260),
            'lps22hb_temperature': regenerateValueMaxMin(self._data['lps22hb_temperature'], 0.2, -30, 100),
            'ads1015_a0': regenerateValueMaxMin(self._data['ads1015_a0'], 0.1, 600, 15000),
            'ads1015_a1': regenerateValueMaxMin(self._data['ads1015_a1'], 0.1, 900, 1000),
            'ads1015_a2': regenerateValueMaxMin(self._data['ads1015_a2'], 0.1, 900, 1000),
            'ads1015_a3': regenerateValueMaxMin(self._data['ads1015_a3'], 0.1, 900, 1000),
            'shtc3_temperature': regenerateValueMaxMin(self._data['shtc3_temperature'], 0.1, -10, 50),
            'shtc3_humidity': regenerateValueMaxMin(self._data['shtc3_humidity'], 0.1, 0, 100),
            'tcs34087_rgb_r': regenerateValueMaxMin(self._data['tcs34087_rgb_r'], 0.1, 0, 255),
            'tcs34087_rgb_g': regenerateValueMaxMin(self._data['tcs34087_rgb_g'], 0.1, 0, 255),
            'tcs34087_rgb_b': regenerateValueMaxMin(self._data['tcs34087_rgb_b'], 0.1, 0, 255),
            'tcs34087_c': regenerateValueMaxMin(self._data['tcs34087_c'], 0.1, 0, 65535),
            'tcs34087_rgb565': regenerateValueMaxMin(self._data['tcs34087_rgb565'], 0.1, 0, 65535),
            'tcs34087_rgb888': regenerateValueMaxMin(self._data['tcs34087_rgb888'], 0.1, 0, 16777215),
            'tcs34087_lux': regenerateValueMaxMin(self._data['tcs34087_lux'], 0.1, 0, 100),
            'tcs34087_lux_interrupt': '0',
            'tcs34087_color_temp': regenerateValueMaxMin(self._data['tcs34087_color_temp'], 0.1, 0, 3394.3757313660644),
        }
        return True


if __name__ == '__main__':
    v = DeviceSimulator()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))

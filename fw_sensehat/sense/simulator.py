#!/usr/bin/python3

from fw_sensehat.sense.device import Device
from fw_sensehat.base.commons import regenerateValueMaxMin


class DeviceSimulator(Device):

    def __init__(self):
        super().__init__(False)
        self._data = {
            'hardcoded_model': 'SenseHat(c)',
            'imu_roll': '0.06830104668952965',
            'imu_pitch': '-0.727970848515366',
            'imu_yaw': '160.75668277388567',
            'imu_acceleration_x': '0',
            'imu_acceleration_y': '0',
            'imu_acceleration_z': '0',
            'imu_gyroscope_x': '0',
            'imu_gyroscope_y': '0',
            'imu_gyroscope_z': '0',
            'imu_magnetic_x': '0',
            'imu_magnetic_y': '0',
            'imu_magnetic_z': '0',
            'imu_qmi_temperature': '23.8203125',
            'lps22hb_pressure': '996.468505859375',
            'lps22hb_temperature': '26.15',
            'ads1015_a0': '0',
            'ads1015_a1': '0',
            'ads1015_a2': '0',
            'ads1015_a3': '0',
            'shtc3_temperature': '23.8203125',
            'shtc3_humidity': '29.8541224',
            'tcs34087_rgb_r': '21',
            'tcs34087_rgb_g': '10',
            'tcs34087_rgb_b': '10',
            'tcs34087_c': '1044',
            'tcs34087_rgb565': '4161',
            'tcs34087_rgb888': '1378826',
            'tcs34087_lux': '0',
            'tcs34087_lux_interrupt': '0',
            'tcs34087_color_temp': '1507.0112429731416'
        }
        self._is_connected = True

    def init_chips(self):
        self._is_connected = True

    def refresh(self, reset_data=False) -> bool:
        self._data = {
            'hardcoded_model': 'SenseHat(c)',
            'imu_roll': str(regenerateValueMaxMin(self._data['imu_roll'], 0.1, -180, 180)),
            'imu_pitch': str(regenerateValueMaxMin(self._data['imu_pitch'], 0.1, -180, 180)),
            'imu_yaw': str(regenerateValueMaxMin(self._data['imu_yaw'], 0.1, -180, 180)),
            'imu_acceleration_x': str(int(regenerateValueMaxMin(self._data['imu_acceleration_x'], 1, 0, 20000))),
            'imu_acceleration_y': str(int(regenerateValueMaxMin(self._data['imu_acceleration_y'], 1, 0, 20000))),
            'imu_acceleration_z': str(int(regenerateValueMaxMin(self._data['imu_acceleration_z'], 1, 0, 20000))),
            'imu_gyroscope_x': str(int(regenerateValueMaxMin(self._data['imu_gyroscope_x'], 1, -2048, 2048))),
            'imu_gyroscope_y': str(int(regenerateValueMaxMin(self._data['imu_gyroscope_y'], 1, -2048, 2048))),
            'imu_gyroscope_z': str(int(regenerateValueMaxMin(self._data['imu_gyroscope_z'], 1, -2048, 2048))),
            'imu_magnetic_x': str(int(regenerateValueMaxMin(self._data['imu_magnetic_x'], 0.1, 0, 10))),
            'imu_magnetic_y': str(int(regenerateValueMaxMin(self._data['imu_magnetic_y'], 0.1, 0, 10))),
            'imu_magnetic_z': str(int(regenerateValueMaxMin(self._data['imu_magnetic_z'], 0.1, 0, 10))),
            'imu_qmi_temperature': str(regenerateValueMaxMin(self._data['imu_qmi_temperature'], 0.2, -30, 100)),
            'lps22hb_pressure': str(regenerateValueMaxMin(self._data['lps22hb_pressure'], 0.1, 260, 1260)),
            'lps22hb_temperature': str(regenerateValueMaxMin(self._data['lps22hb_temperature'], 0.2, -30, 100)),
            'ads1015_a0': str(int(regenerateValueMaxMin(self._data['ads1015_a0'], 1, 0, 65536))),
            'ads1015_a1': str(int(regenerateValueMaxMin(self._data['ads1015_a1'], 1, 0, 65536))),
            'ads1015_a2': str(int(regenerateValueMaxMin(self._data['ads1015_a2'], 1, 0, 65536))),
            'ads1015_a3': str(int(regenerateValueMaxMin(self._data['ads1015_a3'], 1, 0, 65536))),
            'shtc3_temperature': str(regenerateValueMaxMin(self._data['shtc3_temperature'], 0.1, -10, 50)),
            'shtc3_humidity': str(regenerateValueMaxMin(self._data['shtc3_humidity'], 0.1, 0, 100)),
            'tcs34087_rgb_r': str(int(regenerateValueMaxMin(self._data['tcs34087_rgb_r'], 0.1, 0, 255))),
            'tcs34087_rgb_g': str(int(regenerateValueMaxMin(self._data['tcs34087_rgb_g'], 0.1, 0, 255))),
            'tcs34087_rgb_b': str(int(regenerateValueMaxMin(self._data['tcs34087_rgb_b'], 0.1, 0, 255))),
            'tcs34087_c': str(int(regenerateValueMaxMin(self._data['tcs34087_c'], 0.1, 0, 65535))),
            'tcs34087_rgb565': str(int(regenerateValueMaxMin(self._data['tcs34087_rgb565'], 0.1, 0, 65535))),
            'tcs34087_rgb888': str(int(regenerateValueMaxMin(self._data['tcs34087_rgb888'], 0.1, 0, 16777215))),
            'tcs34087_lux': str(int(regenerateValueMaxMin(self._data['tcs34087_lux'], 1, 0, 10000))),
            'tcs34087_lux_interrupt': '0',
            'tcs34087_color_temp': str(regenerateValueMaxMin(self._data['tcs34087_color_temp'], 0.1, 0, 10000)),
        }
        return True


if __name__ == '__main__':
    v = DeviceSimulator()
    print("{}# [{}CONNECTED]: {}".format(v.device_type,
                                         "" if v.is_connected else "NOT ",
                                         v.latest_data["V"]))

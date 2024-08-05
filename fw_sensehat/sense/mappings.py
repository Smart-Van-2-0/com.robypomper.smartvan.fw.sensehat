#!/usr/bin/python3

from fw_sensehat.commons import *
from ._definitions import *
from ._dbus_descs import *
from ._parsers import *

# Given an PID, this object returns all his info and meta-data
PID = {
    "SenseHat(c)": {"model": "Sense Hat (c)", "type": DEV_TYPE_SenseHat_c,
                    "dbus_iface": DEV_IFACE_SenseHat_c, "dbus_desc": DEV_DBUS_DESC_SenseHat},
}

PROPS_CODES = {
    "hardcoded_model": {"name": "model", "desc": "Device model (hardcoded)",
                        "parser": props_parser_str},

    "imu_roll": {"name": "roll", "desc": "IMU Roll axis",
                 "parser": props_parser_float},
    "imu_pitch": {"name": "pitch", "desc": "IMU Pitch axis",
                  "parser": props_parser_float},
    "imu_yaw": {"name": "yaw", "desc": "IMU Yaw axis",
                "parser": props_parser_float},
    "imu_acceleration_x": {"name": "acceleration_x", "desc": "IMU Acceleration x axis",
                           "parser": props_parser_int},
    "imu_acceleration_y": {"name": "acceleration_y", "desc": "IMU Acceleration y axis",
                           "parser": props_parser_int},
    "imu_acceleration_z": {"name": "acceleration_z", "desc": "IMU Acceleration z axis",
                           "parser": props_parser_int},
    "imu_gyroscope_x": {"name": "gyroscope_x", "desc": "IMU Gyroscope x axis",
                        "parser": props_parser_int},
    "imu_gyroscope_y": {"name": "gyroscope_y", "desc": "IMU Gyroscope y axis",
                        "parser": props_parser_int},
    "imu_gyroscope_z": {"name": "gyroscope_z", "desc": "IMU Gyroscope z axis",
                        "parser": props_parser_int},
    "imu_magnetic_x": {"name": "magnetic_x", "desc": "IMU Magnetic x axis",
                       "parser": props_parser_int},
    "imu_magnetic_y": {"name": "magnetic_y", "desc": "IMU Magnetic y axis",
                       "parser": props_parser_int},
    "imu_magnetic_z": {"name": "magnetic_z", "desc": "IMU Magnetic z axis",
                       "parser": props_parser_int},
    "imu_qmi_temperature": {"name": "qmu_temperature", "desc": "IMU Temperature",
                            "parser": props_parser_float},

    "lps22hb_pressure": {"name": "pressure", "desc": "LPS22HB Pressure",
                         "parser": props_parser_float},
    "lps22hb_temperature": {"name": "temperature", "desc": "LPS22HB Temperature",
                            "parser": props_parser_float},

    "ads1015_a0": {"name": "analog_0", "desc": "ADS1015 Analog input 0",
                   "parser": props_parser_int},
    "ads1015_a1": {"name": "analog_1", "desc": "ADS1015 Analog input 1",
                   "parser": props_parser_int},
    "ads1015_a2": {"name": "analog_2", "desc": "ADS1015 Analog input 2",
                   "parser": props_parser_int},

    "ads1015_a3": {"name": "analog_3", "desc": "ADS1015 Analog input 3",
                   "parser": props_parser_int},

    "shtc3_temperature": {"name": "temperature", "desc": "SHTC3 Temperature",
                   "parser": props_parser_float},
    "shtc3_humidity": {"name": "humidity", "desc": "SHTC3 Humidity",
                   "parser": props_parser_float},

    "tcs34087_rgb_r": {"name": "lux_rgb_r", "desc": "TCS34087 RGB r",
                       "parser": props_parser_int},
    "tcs34087_rgb_g": {"name": "lux_rgb_g", "desc": "TCS34087 RGB g",
                       "parser": props_parser_int},
    "tcs34087_rgb_b": {"name": "lux_rgb_b", "desc": "TCS34087 RGB b",
                       "parser": props_parser_int},
    "tcs34087_c": {"name": "lux_c", "desc": "TCS34087 Lux c",
                   "parser": props_parser_int},
    "tcs34087_rgb565": {"name": "lux_rgb_565", "desc": "TCS34087 RGB 565",
                        "parser": props_parser_int},
    "tcs34087_rgb888": {"name": "lux_rgb_888", "desc": "TCS34087 RGB 888",
                        "parser": props_parser_int},
    "tcs34087_lux": {"name": "lux", "desc": "TCS34087 Lux",
                     "parser": props_parser_int},
    "tcs34087_lux_interrupt": {"name": "lux_interrupt", "desc": "TCS34087 Lux interrupt",
                               "parser": props_parser_float},
    "tcs34087_color_temp": {"name": "lux_color_temp", "desc": "TCS34087 color temperature",
                            "parser": props_parser_float},

}

CALC_PROPS_CODES = {
    # N/A
}

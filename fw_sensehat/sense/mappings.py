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
    "hardcoded_model": {"name": "model", "desc": "Model (hardcoded)",
                        "parser": props_parser_str},

    "imu_roll": {"name": "roll", "desc": "IMU roll",
                 "parser": props_parser_float},
    "imu_pitch": {"name": "pitch", "desc": "IMU pitch",
                  "parser": props_parser_float},
    "imu_yaw": {"name": "yaw", "desc": "IMU yaw",
                "parser": props_parser_float},
    "imu_acceleration_x": {"name": "acceleration_x", "desc": "IMU acceleration_x",
                           "parser": props_parser_int},
    "imu_acceleration_y": {"name": "acceleration_y", "desc": "IMU acceleration_y",
                           "parser": props_parser_int},
    "imu_acceleration_z": {"name": "acceleration_z", "desc": "IMU acceleration_z",
                           "parser": props_parser_int},
    "imu_gyroscope_x": {"name": "gyroscope_x", "desc": "IMU gyroscope_x",
                        "parser": props_parser_int},
    "imu_gyroscope_y": {"name": "gyroscope_y", "desc": "IMU gyroscope_y",
                        "parser": props_parser_int},
    "imu_gyroscope_z": {"name": "gyroscope_z", "desc": "IMU gyroscope_z",
                        "parser": props_parser_int},
    "imu_magnetic_x": {"name": "magnetic_x", "desc": "IMU magnetic_x",
                       "parser": props_parser_float},
    "imu_magnetic_y": {"name": "magnetic_y", "desc": "IMU magnetic_y",
                       "parser": props_parser_float},
    "imu_magnetic_z": {"name": "magnetic_z", "desc": "IMU magnetic_z",
                       "parser": props_parser_float},
    "imu_qmi_temperature": {"name": "qmu_temperature", "desc": "IMU qmi temperature",
                            "parser": props_parser_float},

    "lps22hb_pressure": {"name": "pressure", "desc": "LPS22HB pressure",
                         "parser": props_parser_float},
    "lps22hb_temperature": {"name": "temperature", "desc": "LPS22HB temperature",
                            "parser": props_parser_float},

    "ads1015_a0": {"name": "analog_0", "desc": "ADS1015 input 0",
                   "parser": props_parser_int},
    "ads1015_a1": {"name": "analog_1", "desc": "ADS1015 input 1",
                   "parser": props_parser_int},
    "ads1015_a2": {"name": "analog_2", "desc": "ADS1015 input 2",
                   "parser": props_parser_int},
    "ads1015_a3": {"name": "analog_3", "desc": "ADS1015 input 3",
                   "parser": props_parser_int},

    "tcs34087_rgb_r": {"name": "lux_rgb_r", "desc": "TCS34087 rgb r",
                       "parser": props_parser_int},
    "tcs34087_rgb_g": {"name": "lux_rgb_g", "desc": "TCS34087 rgb g",
                       "parser": props_parser_int},
    "tcs34087_rgb_b": {"name": "lux_rgb_b", "desc": "TCS34087 rgb b",
                       "parser": props_parser_int},
    "tcs34087_c": {"name": "lux_c", "desc": "TCS34087 c",
                   "parser": props_parser_int},
    "tcs34087_rgb565": {"name": "lux_rgb_565", "desc": "TCS34087 rgb 565",
                        "parser": props_parser_int},
    "tcs34087_rgb888": {"name": "lux_rgb_888", "desc": "TCS34087 rgb 888",
                        "parser": props_parser_int},
    "tcs34087_lux": {"name": "lux", "desc": "TCS34087 lux",
                     "parser": props_parser_int},
    "tcs34087_lux_interrupt": {"name": "lux_interrupt", "desc": "TCS34087 lux interrupt",
                               "parser": props_parser_float},
    "tcs34087_color_temp": {"name": "lux_color_temp", "desc": "TCS34087 color temperature",
                            "parser": props_parser_float},

}

CALC_PROPS_CODES = {
    # N/A
}

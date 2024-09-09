#!/usr/bin/python3


# Calculation defaults and constants

BIT_COUNT = 12
MAX_VALUE = 2 ** BIT_COUNT - 1


# Calculation methods

def calc_analog_0_perc(property_cache) -> float:
    return calc_analog_perc(property_cache, "analog_0")


def calc_analog_1_perc(property_cache) -> float:
    return calc_analog_perc(property_cache, "analog_1")


def calc_analog_2_perc(property_cache) -> float:
    return calc_analog_perc(property_cache, "analog_2")


def calc_analog_3_perc(property_cache) -> float:
    return calc_analog_perc(property_cache, "analog_3")


def calc_analog_perc(property_cache, origin_prop) -> float:
    try:
        analog_val = property_cache[origin_prop]['value']
        return round((analog_val / MAX_VALUE) * 100, 2)
    except KeyError as err:
        raise ValueError("Missing required property: {".format(err))
    except Exception:
        raise ValueError("Can't calculate '{}' <raw value: {}> into percent".format(origin_prop, analog_val))
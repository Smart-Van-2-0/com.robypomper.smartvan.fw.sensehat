#!/usr/bin/python3


def calc_temperature(property_cache) -> float:
    try:
        return property_cache['temperature_2']['value']
    except KeyError as err:
        try:
            return property_cache['temperature_1']['value']
        except KeyError as err2:
            raise ValueError("Missing required properties: {} or {}".format(err, err2))

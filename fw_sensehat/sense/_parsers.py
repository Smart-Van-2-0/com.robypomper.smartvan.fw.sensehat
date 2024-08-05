#!/usr/bin/python3


def props_parser_vin(raw_value: str) -> bool:
    try:
        if raw_value.upper() == "GOOD":
            return True
        elif raw_value.upper() == "NG":
            return False
        else:
            raise ValueError("Can't cast '{}' into {}, invalid value".format(raw_value, "float"))
    except Exception:
        raise ValueError("Can't cast '{}' into {}".format(raw_value, "float"))


def calc_temperature(property_cache) -> float:
    try:
        return property_cache['temperature_2']['value']
    except KeyError as err:
        try:
            return property_cache['temperature_1']['value']
        except KeyError as err2:
            raise ValueError("Missing required properties: {} or {}".format(err, err2))

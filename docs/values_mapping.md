# FW Sense Hat - Values Mapping

The properties exposed on the DBus vary depending on
the [type of device](supported_devices.md). A description of the
DBus object to be exposed is defined for each type of device. The DBus object
definitions are specified in the
[_dbus_descs.py](/fw_sensehat/sense/_dbus_descs.py) file.

During the `main_loop`, this script refresh the device's data and parse any
property found, if the property value is update the script sends the property
update to the DBus. To parse the property it uses the info contained into
the`PROPS_CODE` table. Sometime, it can trigger an exception because the updated
property is not present into the DBus object definitions. In this case add the
property to the DBus object definitions or fix the `PROPS_CODES` table.

## DBus properties

Exposed properties can be of two types: direct or calculated. Direct properties
are exported as they come from the device. Calculated properties are the result
of an elaboration.

### Direct

Direct properties are defined into the `PROPS_CODES` table into
the [mappings.py](/fw_sensehat/sense/mappings.py) file.

For each property are defined following fields:

* `KEY`: property name on device side
* `name`: property name on DBus
* `desc`: human-readable description of the property
* `parser`: the method to use to parse the value read from the device

| Prop.'s KEY              | Prop.'s Name on DBus | Description                | Parser method        |
|--------------------------|----------------------|----------------------------|----------------------|
| `hardcoded_model`        | `model`              | Device model (hardcoded)   | `props_parser_str`   |
| `imu_roll`               | `roll`               | IMU Roll axis              | `props_parser_float` |
| `imu_pitch`              | `pitch`              | IMU Pitch axis             | `props_parser_float` |
| `imu_yaw`                | `yaw`                | IMU Yaw axis               | `props_parser_float` |
| `imu_acceleration_x`     | `acceleration_x`     | IMU Acceleration x axis    | `props_parser_int`   |
| `imu_acceleration_y`     | `acceleration_y`     | IMU Acceleration y axis    | `props_parser_int`   |
| `imu_acceleration_z`     | `acceleration_z`     | IMU Acceleration z axis    | `props_parser_int`   |
| `imu_gyroscope_x`        | `gyroscope_x`        | IMU Gyroscope x axis       | `props_parser_int`   |
| `imu_gyroscope_y`        | `gyroscope_y`        | IMU Gyroscope y axis       | `props_parser_int`   |
| `imu_gyroscope_z`        | `gyroscope_z`        | IMU Gyroscope z axis       | `props_parser_int`   |
| `imu_magnetic_x`         | `magnetic_x`         | IMU Magnetic x axis        | `props_parser_int`   |
| `imu_magnetic_y`         | `magnetic_y`         | IMU Magnetic y axis        | `props_parser_int`   |
| `imu_magnetic_z`         | `magnetic_z`         | IMU Magnetic z axis        | `props_parser_int`   |
| `imu_qmi_temperature`    | `qmu_temperature`    | IMU Temperature            | `props_parser_float` |
| `lps22hb_pressure`       | `pressure`           | LPS22HB Pressure           | `props_parser_float` |
| `lps22hb_temperature`    | `temperature_1`      | LPS22HB Temperature        | `props_parser_float` |
| `ads1015_a0`             | `analog_0`           | ADS1015 Analog input 0     | `props_parser_int`   |
| `ads1015_a1`             | `analog_1`           | ADS1015 Analog input 1     | `props_parser_int`   |
| `ads1015_a2`             | `analog_2`           | ADS1015 Analog input 2     | `props_parser_int`   |
| `ads1015_a3`             | `analog_3`           | ADS1015 Analog input 3     | `props_parser_int`   |
| `shtc3_temperature`      | `temperature_2`      | SHTC3 Temperature          | `props_parser_float` |
| `shtc3_humidity`         | `humidity`           | SHTC3 Humidity             | `props_parser_float` |
| `tcs34087_rgb_r`         | `lux_rgb_r`          | TCS34087 RGB r             | `props_parser_int`   |
| `tcs34087_rgb_g`         | `lux_rgb_g`          | TCS34087 RGB g             | `props_parser_int`   |
| `tcs34087_rgb_b`         | `lux_rgb_b`          | TCS34087 RGB b             | `props_parser_int`   |
| `tcs34087_c`             | `lux_c`              | TCS34087 Lux c             | `props_parser_int`   |
| `tcs34087_rgb565`        | `lux_rgb_565`        | TCS34087 RGB 565           | `props_parser_int`   |
| `tcs34087_rgb888`        | `lux_rgb_888`        | TCS34087 RGB 888           | `props_parser_int`   |
| `tcs34087_lux`           | `lux`                | TCS34087 Lux               | `props_parser_int`   |
| `tcs34087_lux_interrupt` | `lux_interrupt`      | TCS34087 Lux interrupt     | `props_parser_int`   |
| `tcs34087_color_temp`    | `lux_color_temp`     | TCS34087 Color temperature | `props_parser_float` |

Parser methods are defined into [_parsers.py](/fw_sensehat/sense/_parsers.py)
file. Depending on which DBus property's they are mapped for, they can return
different value's types.<br/>
Custom types are defined into
the [_definitions.py](/fw_sensehat/sense/_definitions.py) file.

### Calculated

Calculated properties are special values that can be elaborated starting from
other properties (also other calculated properties). When a property is updated,
the script checks if there is some calculated property that depends on it. If
any, then the script calculate the dependant property.

For each calculated property are defined following fields:

* `KEY`: calculated property name on DBus
* `name`: calculated property name (not used)
* `desc`: human-readable description of the property
* `depends_on`: the list of properties on which the current property depends
* `calculator`: the method to use to elaborate the property

| Prop.'s Name on DBus | Description             | Depends on                       | Calculator method  |
|----------------------|-------------------------|----------------------------------|--------------------|
| `temperature`        | Environment temperature | `temperature_2`, `temperature_1` | `calc_temperature` |

All methods used to elaborate the properties, receives the properties cache as
param. So they can use that list to get all properties read from the device (
also other calculated properties).

## Properties by DBus Object description

This is the table containing all properties handled by this script. For each
property, the table define if it will be exported by the column's device type.

| Prop.'s Name on DBus | Type   | Sense Hat c |
|----------------------|--------|-------------|
| `model`              | string | Yes         |
| `roll`               | double | Yes         |
| `pitch`              | double | Yes         |
| `yaw`                | double | Yes         |
| `acceleration_x`     | int    | Yes         |
| `acceleration_y`     | int    | Yes         |
| `acceleration_z`     | int    | Yes         |
| `gyroscope_x`        | int    | Yes         |
| `gyroscope_y`        | int    | Yes         |
| `gyroscope_z`        | int    | Yes         |
| `magnetic_x`         | int    | Yes         |
| `magnetic_y`         | int    | Yes         |
| `magnetic_z`         | int    | Yes         |
| `qmu_temperature`    | double | Yes         |
| `pressure`           | double | Yes         |
| `temperature_1`      | double | Yes         |
| `analog_0`           | int    | Yes         |
| `analog_1`           | int    | Yes         |
| `analog_2`           | int    | Yes         |
| `analog_3`           | int    | Yes         |
| `temperature_2`      | double | Yes         |
| `humidity`           | double | Yes         |
| `lux_rgb_r`          | int    | Yes         |
| `lux_rgb_g`          | int    | Yes         |
| `lux_rgb_b`          | int    | Yes         |
| `lux_c`              | int    | Yes         |
| `lux_rgb_565`        | int    | Yes         |
| `lux_rgb_888`        | int    | Yes         |
| `lux`                | int    | Yes         |
| `lux_interrupt`      | int    | Yes         |
| `lux_color_temp`     | double | Yes         |

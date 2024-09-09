# FW Sense Hat - Changelog

[README](README.md) | [CHANGELOG](CHANGELOG.md) | [TODOs](TODOs.md) | [LICENCE](LICENCE.md)


## Version 1.0.1

* Fixed wrong links in docs
* Updated base firmware: repoSync
* Updated base code for all integrated chips (QMI8658C, AK09918, SHTC3, ADS1015, LPS22HB, TCS34087)
* Added property: temperature_2 and humidity for SHTC3
* Updated property: temperature to temperature_1 for LPS22HB
* Added property: temperature calculated from temperature_2 and temperature_1
* Various fixes on simulator and parsers
* Fixed HALT signal handling

You can find the logs of this version into the [docs/logs](docs/logs) folder.

## Version 1.0.0

* Copied files from the [com.robypomper.smartvan.fw.sensepack_v3](https://github.com/Smart-Van-2-0/com.robypomper.smartvan.fw.sensepack_v3) repo
* Rearranged scripts files and grouped common code
* Implemented Device class for Sense Hat over I2C
* Added supported_devices.md and values_mapping.md as documentation pages

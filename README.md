# FW Sense Hat

Simple Python module that read data
from [Sense Hat](https://www.waveshare.com/sense-hat-c.htm) and share them on
the local DBus.<br />
This repository is part of
the [Smart Van Project](https://smartvan.johnosproject.org/).

**FW Name:** FW Sense Hat<br />
**FW Group:** com.robypomper.smartvan.fw.sensehat<br />
**FW Version:** 1.0.1-DEV

[README](README.md) | [CHANGELOG](CHANGELOG.md) | [TODOs](TODOs.md) | [LICENCE](LICENCE.md)

Once ran, this script **reads data from the Sense Hat board via I2C then notify
the DBus with updated values**. The Sense Hat is a crucial component equipped
with a variety of sensors and accessible ICs through the I2C protocol. Each of
these components has its dedicated Python file (located in
the `fw_sensehat/sense/chip` folder). These files facilitate the reading and
processing of raw data collected by the sensors. More info 
on [Supported devices](/docs/supported_devices.md)
and [value mapping](/docs/values_mapping.md).

## Run

This is a Python script, so `python` is required to run it.

```shell
$ python --version
# if not installed, then run
$ sudo apt-get install python3 python3-pip
```

In addition, some other package must be installed in order to configure
python's dependencies like `PyGObject` or `pydbus`. If you are using a
debian/ubuntu based distribution, then you can run:

```shell
$ sudo apt-get install libcairo2-dev libgirepository1.0-dev dbus-x11
```

Once Python was installed on your machine, you can install the script's
requirements globally or create a dedicated `venv`.

```shell
# Init venv (Optional)
$ python -m venv venev
$ source venv/bin/activate

# Install script's requirements
$ pip install -r requirements.txt
```

Now, you are ready to run the script with the command:

```shell
$ python run.py

or alternative options
$ python run.py --quiet
$ python run.py --debug --simulate
$ python run.py  --dbus-name com.custom.bus --dbus-obj-path /custom/path --dbus-iface com.custom.IFace
```

For script's [remote usage](docs/remote_usage.md) please see the dedicated page.

Defaults DBus params are:

* DBus Name: `com.waveshare.sensehat`
* DBus Obj Path: `DEV_TYPE_*` as device code (eg: `Sense Hat c` become
  `/sense_hat_c`, see [Supported devices](/docs/supported_devices.md) for
  the full list of `DEV_TYPE_*` values)
* DBus Interface: `DEV_IFACE_*` (eg: `com.waveshare.sensehat_c`,
  see [Supported devices](/docs/supported_devices.md) for the full list of
  `DEV_IFACE_*` values)

### Script's arguments

The `run.py` script accept following arguments:

* `-h`, `--help`: show this help message and exit
* `-v`, `--version`: show version and exit
* `--simulate`: Simulate a Sense Hat (C) Device  (default: `False`)
* `--dbus-name DBUS_NAME`: DBus name to connect to (Default: `com.waveshare.sense`)
* `--dbus-obj-path DBUS_OBJ_PATH`: DBus object path to use for object
  publication (Default: the `device_type_code` string)
* `--dbus-iface DBUS_IFACE`: DBus object's interface (Default: current device's
  `dbus_iface`)
* `--dev`: enable development mode, increase log messages
* `--debug`: Set log level to debug
* `--quiet`: Set log level to error and

## Develop

The main goal for this script is to link the Device's protocol to the DBus.
So, in addition to the main script, all other files are related to the Device
or to the DBus protocols.

Module's files can be grouped in 2 categories:

**Definitions:**

* [sense/mappings.py](/fw_sensehat/sense/mappings.py):
  definition of `PID`, `PROPS_CODES` and `CALC_PROPS_CODES` tables
* [sense/_definitions.py](/fw_sensehat/sense/_definitions.py):
  definitions of supported devices, DUbus ifaces and custom properties types
* [sense/_parsers.py](/fw_sensehat/sense/_parsers.py):
  custom properties parsers
* [sense/_calculated.py](/fw_sensehat/sense/_calculated.py):
  custom properties calculators and data generator methods for simulator
* [sense/_dbus_descs.py](/fw_sensehat/sense/_dbus_descs.py):
  definition of DBus iface's descriptors

**Operations:**

* [run.py](run.py):
  main firmware script
* [sense/device.py](/fw_sensehat/sense/device.py):
  class that represent the device
* [sense/simulator.py](/fw_sensehat/sense/simulator.py):
  class that represent the simulated device
* [dbus/obj.py](/fw_sensehat/dbus/obj.py):
  class that represent aDBus object to publish
* [dbus/daemon.py](/fw_sensehat/dbus/daemon.py):
  methods to handle the DBus daemon
* [commons.py](/fw_sensehat/commons.py):
  commons properties parsers and simulator methods
* [device.py](/fw_sensehat/device.py):
  base class for devices
* [device_serial.py](/fw_sensehat/device_serial.py):
  base implementation for serial devices

## References

* [Sense Hat (C) Wiki](https://www.waveshare.com/wiki/Sense_HAT_(C))
  - Breakout board for Raspberry Pi, featuring several onboard sensors and ICs
* [QMI8658C](https://www.qstcorp.com/upload/pdf/202202/%EF%BC%88%E5%B7%B2%E4%BC%A0%EF%BC%89QMI8658C%20datasheet%20rev%200.9.pdf)
  - 6D Inertial Measurement Unit with Motion Co-Processor and Sensor Fusion
* [AK09918](https://www.mouser.it/datasheet/2/1431/ak09918c_en_datasheet-3010173.pdf)
  - 3-Axis Electronic Compass)
* [SHTC3](https://www.mouser.it/datasheet/2/682/seri_s_a0003561073_1-2291167.pdf)
  - Humidity and Temperature Sensor IC
* [LPS22HB](https://www.mouser.it/datasheet/2/389/lps22hb-1849683.pdf)
  - MEMS nano pressure sensor: 260-1260 hPa absolute digital output barometer
* [TCS34725](https://4donline.ihs.com/images/VipMasterIC/IC/AMSY/AMSY-S-A0017934720/AMSY-S-A0017934789-1.pdf?hkey=52A5661711E402568146F3353EA87419)
  - ALS/Color Sensor with Selective Flicker Detection
* [SGM58031](https://www.sg-micro.com/uploads/soft/20230515/1684139579.pdf)
  - Ultra-Small, Low-Power, 16-Bit Analog-to-DigitalConverter with Internal Reference

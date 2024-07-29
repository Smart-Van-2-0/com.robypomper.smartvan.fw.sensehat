# FW Sense Hat - Supported devices

During the device initialization, this script uses the `hardcoded_model`, a
pre-set hardcoded value (`SenseHat(c)`) as the **product PID of the connected
device**.
The **device information is then retrieved from the PID mapping** in the
[mappings.py](/fw_sensehat/sense/mappings.py) file, this file is based on
the [Devices by MODEL](#devices-by-model) tables.<br/>
Then, those info are used to initialize the DBus object with the correspondent
DBus iface and description. Both, the iface and the object description are
defined into the `PID` mapping.

* `model`: human-readable name of the exact model
* `type`: devices code to group similar devices
  from [_definitions.py](/fw_sensehat/sense/_definitions.py) as `DEV_TYPE_*`
* `dbus_iface`: a string defining the DBus iface<br/>
  from [_definitions.py](/fw_sensehat/sense/_definitions.py) as `DEV_IFACE_*`
* `dbus_desc`: a string defining the DBus object's description<br/>
  [dbus_definitions.py](/fw_sensehat/sense/_dbus_descs.py) as `DEV_DBUS_DESC_*`

## Device types

Here, you can find the list of all devices types available. Any product MODEL
from [Devices by MODEL](#devices-by-model) section is mapped into a device type
using the `PID` table from the [mappings.py](/fw_sensehat/sense/mappings.py)
file.
More details on DBus definitions and their properties can be found on
the [Values Mapping](values_mapping.md#properties-by-dbus-object-description)
page.

| Type's Constant       | Type's Name | DBus's Iface             | DBus's Description       |
|-----------------------|-------------|--------------------------|--------------------------|
| `DEV_TYPE_SenseHat_c` | Sense Hat c | com.waveshare.sensehat_c | `DEV_DBUS_DESC_SenseHat` |

## Devices by MODEL

At the current version, any 'Sense Hat (c)' board is supported. To support more
versions, please update the pre-set hardcoded value `hardcoded_model` and the
`PID` table into the [mappings.py](/fw_sensehat/sense/mappings.py) file.

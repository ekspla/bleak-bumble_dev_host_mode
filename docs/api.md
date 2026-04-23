# API Reference

This section contains the API documentation for `bleak_bumble`.

## Core Classes and Functions

### TransportScheme

Enumeration of supported transport schemes.

**Values:**
- `TCP_SERVER` - TCP server transport
- `TCP_CLIENT` - TCP client transport
- `SERIAL` - Serial port transport
- `USB` - USB transport
- `ANDROID_NETSIM` - Android emulator netsim transport
- `VHCI` - Virtual HCI transport (Linux only)

### BumbleTransportCfg

Configuration class for Bumble transport settings.

**Constructor:**
```python
BumbleTransportCfg(scheme: TransportScheme, arguments: str = "")
```

**Parameters:**
- `scheme` - The transport scheme to use
- `arguments` - Transport-specific arguments (e.g., "127.0.0.1:1000" for TCP)

**Attributes:**
- `scheme` - The configured transport scheme
- `arguments` - The transport arguments

### get_default_transport_cfg()

Returns the default transport configuration based on environment variables.

**Returns:** `BumbleTransportCfg` or `None`

Reads from `BLEAK_BUMBLE` environment variable in format `scheme:arguments`.

### is_host_mode_enabled_from_env()

Checks if host mode is enabled via environment variables.

**Returns:** `bool`

Returns `True` if `BLEAK_BUMBLE_HOST` environment variable is set to any non-empty value. This function checks the environment configuration rather than providing a default value.

## Scanner Module (`bleak_bumble.scanner`)

### BleakScannerBumble

Bumble backend implementation for BleakScanner.

**Constructor:**
```python
BleakScanner(
    detection_callback: Optional[AdvertisementDataCallback] = None,
    service_uuids: Optional[List[str]] = None,
    scanning_mode: Literal["active", "passive"] = "active",
    backend=BleakScannerBumble,
    cfg: Optional[BumbleTransportCfg] = None,
    host_mode: bool = False,
    **kwargs
)
```

**Parameters:**
- `detection_callback` - Callback for advertisement data
- `service_uuids` - List of service UUIDs to filter for
- `cfg` - Transport configuration (uses default if None)
- `host_mode` - Enable HCI host mode
- `**kwargs` - Additional arguments passed to parent class

**Methods:**

#### `start() -> None`
Start the scanner.  

`scanning_phys=(hci.HCI_LE_1M_PHY, hci.HCI_LE_CODED_PHY)` and `LE_Extended_Scan` are used, if available. 
See Bumble's `device.py` for details.  

#### `stop() -> None` 
Stop the scanner.

#### `get_discovered_devices() -> List[BLEDevice]`
Get list of discovered devices.

## Client Module (`bleak_bumble.client`)

### BleakClientBumble

Bumble backend implementation for BleakClient.

**Constructor:**
```python
BleakClient(
    address_or_ble_device: Union[BLEDevice, str],
    backend=BleakClientBumble,
    cfg: Optional[BumbleTransportCfg] = None,
    host_mode: bool = False,
    phys: Optional[str] = None,
    **kwargs
)
```

**Parameters:**
- `address_or_ble_device` - Device to connect to
- `cfg` - Transport configuration (uses default if None)
- `host_mode` - Enable HCI host mode
- `phys` - For supported controllers, set a comma separated string of '1m', '2m' and 'coded'. 
Preferences for the 1M PHY are always set. See `example/client_change_connection_phy.py` how to use. 
- `**kwargs` - Additional arguments passed to parent class

**Methods:**

#### `connect(**kwargs) -> None`
Connect to the device.

#### `disconnect() -> None`
Disconnect from the device.

#### `get_services(**kwargs) -> BleakGATTServiceCollection`
Get GATT services from the device.

#### `read_gatt_char(characteristic: BleakGATTCharacteristic) -> bytearray`
Read from a GATT characteristic.

#### `read_gatt_descriptor(descriptor: BleakGATTDescriptor, **kwargs) -> bytearray`
Read from a GATT descriptor.

#### `write_gatt_char(characteristic: BleakGATTCharacteristic, data: Union[bytes, bytearray, memoryview], response: bool = True) -> None`
Write to a GATT characteristic.

#### `write_gatt_descriptor(descriptor: BleakGATTDescriptor, data: Buffer) -> None`
Write to a GATT descriptor.

#### `start_notify(characteristic: BleakGATTCharacteristic, callback: NotifyCallback, **kwargs) -> None`
Start notifications for a characteristic.  

- `**kwargs`:
   - `force_indicate: bool = False`: If this is set to True, then Bleak will set up 
a indication request instead of a notification request, given that 
the characteristic supports notifications as well as indications.  

#### `stop_notify(characteristic: BleakGATTCharacteristic) -> None`
Stop notifications for a characteristic.

## Utilities Module (`bleak_bumble`, `bleak_bumble.utils`)

### Utility Functions

Various utility functions for transport configuration, device management, and backend operations.

**Key functions:**
- Transport configuration helpers
- Device address validation
- Backend initialization utilities

## Type Definitions

### AdvertisementDataCallback
```python
Callable[[BLEDevice, AdvertisementData], None]
```
Callback type for handling advertisement data.

### NotifyCallback  
```python
Callable[[int, bytearray], None]
```
Callback type for handling characteristic notifications.

## Constants

### Default Values

#### Default BD Device address  
 - `bleak_bumble.scanner`  
``` Python
SCANNER_BD_ADDR = "F0:F1:F2:F3:F4:F5"
```
 - `bleak_bumble.client`  
``` Python
CLIENT_BD_ADDR = "F0:F1:F2:F3:F4:F5"
```

#### Default Timeouts  
   - Maximum time to wait for a connection to be established  
`bumble.device`  
``` Python
DEVICE_DEFAULT_CONNECT_TIMEOUT                = None  # No timeout
```
`bleak.backends.client.BaseBleakClient`
``` Python
        timeout (float): Timeout for required ``discover`` call. Defaults to 10.0.
```

   - Connection Supervision Timeout  
`bumble.device`
``` Python
DEVICE_DEFAULT_CONNECTION_SUPERVISION_TIMEOUT = 720  # ms
```

   - HCI Command Timeout  
`bumble.device.Device.with_hci`
``` Python
        self.command_timeout = 10  # seconds
```

#### Default MTU  
`bumble.att`
```
ATT_DEFAULT_MTU = 23
```

#### Default Connection Intervals  
`bumble.device`
``` Python
DEVICE_DEFAULT_CONNECTION_INTERVAL_MIN        = 15  # ms
DEVICE_DEFAULT_CONNECTION_INTERVAL_MAX        = 30  # ms
```

## Error Handling

The backend raises standard Bleak exceptions:
- `BleakError` - General Bleak errors

## Environment Variables

### BLEAK_BUMBLE
Format: `scheme:arguments`

Examples:
- `tcp-server:127.0.0.1:1000`
- `serial:/dev/ttyUSB0`
- `usb:0`
- `android-netsim:`
- `vhci:`

### BLEAK_BUMBLE_HOST  
Set to any non-empty value to enable host mode.

Examples:
- `BLEAK_BUMBLE_HOST=1`
- `BLEAK_BUMBLE_HOST=true`

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
BleakScannerBumble(
    detection_callback: Optional[AdvertisementDataCallback] = None,
    service_uuids: Optional[List[str]] = None,
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

#### `stop() -> None` 
Stop the scanner.

#### `get_discovered_devices() -> List[BLEDevice]`
Get list of discovered devices.

## Client Module (`bleak_bumble.client`)

### BleakClientBumble

Bumble backend implementation for BleakClient.

**Constructor:**
```python
BleakClientBumble(
    address_or_ble_device: Union[BLEDevice, str],
    cfg: Optional[BumbleTransportCfg] = None,
    host_mode: bool = False,
    **kwargs
)
```

**Parameters:**
- `address_or_ble_device` - Device to connect to
- `cfg` - Transport configuration (uses default if None)
- `host_mode` - Enable HCI host mode
- `**kwargs` - Additional arguments passed to parent class

**Methods:**

#### `connect(**kwargs) -> bool`
Connect to the device.

#### `disconnect() -> bool`
Disconnect from the device.

#### `get_services(**kwargs) -> BleakGATTServiceCollection`
Get GATT services from the device.

#### `read_gatt_char(char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID]) -> bytearray`
Read from a GATT characteristic.

#### `write_gatt_char(char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID], data: Union[bytes, bytearray, memoryview], response: bool = True) -> None`
Write to a GATT characteristic.

#### `start_notify(char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID], callback: NotifyCallback) -> None`
Start notifications for a characteristic.

#### `stop_notify(char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID]) -> None`
Stop notifications for a characteristic.

## Utilities Module (`bleak_bumble.utils`)

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
- Default timeout: 10.0 seconds
- Default MTU: 517 bytes
- Default connection interval: 30ms

## Error Handling

The backend raises standard Bleak exceptions:
- `BleakError` - General Bleak errors
- `BleakDeviceNotFoundError` - Device not found
- `BleakDBusError` - Backend communication errors

## Environment Variables

### BLEAK_BUMBLE
Format: `scheme:arguments`

Examples:
- `tcp-server:127.0.0.1:1000`
- `serial:/dev/ttyUSB0`
- `android-netsim:`
- `vhci:`

### BLEAK_BUMBLE_HOST  
Set to any non-empty value to enable host mode.

Examples:
- `BLEAK_BUMBLE_HOST=1`
- `BLEAK_BUMBLE_HOST=true`

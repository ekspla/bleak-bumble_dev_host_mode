# Usage

This backend adds support for the [Bumble](https://github.com/google/bumble) Bluetooth Controller Stack from Google. The backend enables support of multiple [bumble transports](https://google.github.io/bumble/transports/index.html) to communicate with a physical or virtual HCI controller.

## Basic Usage

To use the Bumble backend, you need to import the specific Bumble classes:

```python
from bleak import BleakScanner, BleakClient
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

# Create transport configuration
cfg = BumbleTransportCfg(TransportScheme.TCP_SERVER, "127.0.0.1:1000")

# Create scanner with Bumble backend
scanner = BleakScanner(backend=BleakScannerBumble, cfg=cfg)

# Scan for devices
async for device, advertisement_data in scanner.advertisement_data():
    # Create client with Bumble backend
    client = BleakClient(device, backend=BleakClientBumble, cfg=cfg)
    await client.connect()
    # ... do work with client
    await client.disconnect()
```

## Environment Variables

You can also configure the backend using environment variables:

### `BLEAK_BUMBLE`
Set the transport configuration. Format: `scheme:arguments`
Example: `tcp-server:127.0.0.1:1000`

### `BLEAK_BUMBLE_HOST`
Set to any non-empty value to enable host mode.

With environment variables, you can use the default transport configuration:

```python
import os
from bleak_bumble import get_default_transport_cfg
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

# Set environment variable
os.environ["BLEAK_BUMBLE"] = "tcp-server:127.0.0.1:1000"

# Use default configuration
scanner = BleakScanner(backend=BleakScannerBumble)
client = BleakClient(device, backend=BleakClientBumble)
```

## HCI Mode

Bumble can be used either as a Bluetooth HCI Controller or HCI Host. By default, it is used as an HCI Controller. To use it as an HCI Host, set the `host_mode` parameter:

```python
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

cfg = BumbleTransportCfg(TransportScheme.TCP_SERVER, "127.0.0.1:1000")
scanner = BleakScanner(backend=BleakScannerBumble, cfg=cfg, host_mode=True)
client = BleakClient(device, backend=BleakClientBumble, cfg=cfg, host_mode=True)
```

## Transport Schemes

The following transport schemes are supported:

- `TransportScheme.TCP_SERVER` - TCP server transport
- `TransportScheme.TCP_CLIENT` - TCP client transport  
- `TransportScheme.SERIAL` - Serial port transport
- `TransportScheme.USB` - USB transport
- `TransportScheme.ANDROID_NETSIM` - Android emulator netsim
- `TransportScheme.VHCI` - Virtual HCI (Linux only)

Each scheme has different argument requirements. See the [examples](examples.md) for specific usage patterns.

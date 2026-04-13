# Examples

Here are some practical examples of using `bleak_bumble` with different transport layers.

## Zephyr RTOS

Zephyr RTOS supports a [Virtual HCI](https://docs.zephyrproject.org/3.7.0/connectivity/bluetooth/bluetooth-tools.html#running-on-a-virtual-controller-and-native-sim) over a TCP client. To connect your application with Zephyr you need to define a TCP server transport for bumble:

```python
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak import BleakScanner, BleakClient
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

# Create TCP server transport configuration
cfg = BumbleTransportCfg(TransportScheme.TCP_SERVER, "127.0.0.1:1000")

# Create scanner with the transport
scanner = BleakScanner(backend=BleakScannerBumble, cfg=cfg)

async for device, advertisement_data in scanner.advertisement_data():
    client = BleakClient(device, backend=BleakClientBumble, cfg=cfg)
    await client.connect()
    # ... interact with the device
    await client.disconnect()
```

> **Note:** The Zephyr application must be compiled for the `native/posix/64` board. The Bumble controller does not support all HCI LE Commands. For this reason the following configs must be disabled in the Zephyr firmware: `CONFIG_BT_EXT_ADV`, `CONFIG_BT_AUTO_PHY_UPDATE`, `CONFIG_BT_HCI_ACL_FLOW_CONTROL`.

## Android Emulator

The [Android Emulator](https://developer.android.com/studio/run/emulator) supports virtualization of the Bluetooth Controller over gRPC with the android [netsim](https://android.googlesource.com/platform/tools/netsim/) tool:

```python
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak import BleakScanner, BleakClient
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

# Create Android netsim transport configuration
cfg = BumbleTransportCfg(TransportScheme.ANDROID_NETSIM)

# Create scanner with the transport
scanner = BleakScanner(backend=BleakScannerBumble, cfg=cfg)

async for device, advertisement_data in scanner.advertisement_data():
    client = BleakClient(device, backend=BleakClientBumble, cfg=cfg)
    await client.connect()
    # ... interact with the device
    await client.disconnect()
```

## Serial/USB HCI Controller

To use a serial or USB HCI controller that may not be natively supported:

```python
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak import BleakScanner, BleakClient
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

# Create serial transport configuration
cfg = BumbleTransportCfg(TransportScheme.SERIAL, "/dev/ttyUSB0") # For HCI H4 device
#cfg = BumbleTransportCfg(TransportScheme.USB, "0") # For HCI H2 device

# Enable host mode for physical controllers
scanner = BleakScanner(backend=BleakScannerBumble, cfg=cfg, host_mode=True)

async for device, advertisement_data in scanner.advertisement_data():
    client = BleakClient(device, backend=BleakClientBumble, cfg=cfg, host_mode=True)
    await client.connect()
    # ... interact with the device
    await client.disconnect()
```

## Virtual HCI Controller (VHCI)

For Linux systems with VHCI support:

```python
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak import BleakScanner, BleakClient
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

# Create VHCI transport configuration
cfg = BumbleTransportCfg(TransportScheme.VHCI)

scanner = BleakScanner(backend=BleakScannerBumble, cfg=cfg)

async for device, advertisement_data in scanner.advertisement_data():
    client = BleakClient(device, backend=BleakClientBumble, cfg=cfg)
    await client.connect()
    # ... interact with the device
    await client.disconnect()
```

## Simple Device Discovery

A minimal example for device discovery:

```python
import asyncio
from bleak import BleakScanner
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak_bumble.scanner import BleakScannerBumble

async def scan_for_devices():
    cfg = BumbleTransportCfg(TransportScheme.TCP_SERVER, "127.0.0.1:1000")
    
    async def detection_callback(device, advertisement_data):
        print(f"Found device: {device.name} ({device.address})")
    
    scanner = BleakScanner(
        detection_callback=detection_callback,
        backend=BleakScannerBumble,
        cfg=cfg
    )
    
    await scanner.start()
    await asyncio.sleep(10.0)  # Scan for 10 seconds
    await scanner.stop()

# Run the scan
asyncio.run(scan_for_devices())
```

## Environment Variable Configuration

Using environment variables for configuration:

```python
import os
import asyncio
from bleak import BleakScanner, BleakClient
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

# Set environment variables
os.environ["BLEAK_BUMBLE"] = "tcp-server:127.0.0.1:1000"
os.environ["BLEAK_BUMBLE_HOST"] = "1"

async def scan_and_connect():
    # Use environment variable configuration
    scanner = BleakScanner(backend=BleakScannerBumble)
    
    async for device, advertisement_data in scanner.advertisement_data():
        print(f"Connecting to {device.name} ({device.address})")
        client = BleakClient(device, backend=BleakClientBumble)
        await client.connect()
        
        # Read device information
        services = await client.get_services()
        print(f"Found {len(services)} services")
        
        await client.disconnect()
        break  # Connect to first device found

asyncio.run(scan_and_connect())
```

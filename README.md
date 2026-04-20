# bleak_bumble

`bleak_bumble` provides a [Bumble](https://github.com/google/bumble) backend for [Bleak](https://github.com/hbldh/bleak) that enables:

- **Hardware-independent Bluetooth LE support**: Use HCI Controllers (e.g. serial/USB) that are not supported natively by your OS
- **Independent of OS's Bluetooth stack**: Linux/MacOS/Windows; e.g. the same code works on the latest Linux and on the obsolete Windows 7sp1 (BLE not supported natively)
- **Virtual Bluetooth testing**: Perform Bluetooth functional tests without physical hardware using virtual Bluetooth stacks like Android Emulator and Zephyr RTOS  
- **Cross-network connections**: Connect HCI Controllers that are not in the same radio network (virtual or physical)

## Installation

```bash
pip install -e git+https://github.com/vChavezB/bleak-bumble.git#egg=bleak_bumble
```

## Quick Start

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
    client = BleakClient(device, backend=BleakClientBumble, cfg=cfg)
    await client.connect()
    # ... work with device
    await client.disconnect()
```

Instead of using `cfg` and `host_mode`, one can use environmental variables as followings.
```python
import os
# Set environment variables
#os.environ["BLEAK_BUMBLE"] = "serial:/dev/ttyUSB0,1000000,rtscts"
os.environ["BLEAK_BUMBLE"] = "usb:0"
os.environ["BLEAK_BUMBLE_HOST"] = "1"
```
`backend=BleakScannerBumble` and `backend=BleakClientBumble` are necessary in this case.  

## Documentation

- [Installation Guide](docs/installation.md)
- [Usage Instructions](docs/usage.md)  
- [Examples](docs/examples.md)
- [API Reference](docs/api.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

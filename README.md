# bleak_bumble

`bleak_bumble` provides a [Bumble](https://github.com/google/bumble) backend for [Bleak](https://github.com/hbldh/bleak) that enables:

- **Hardware-independent Bluetooth LE support**: Use HCI Controllers (e.g. serial/USB) that are not supported natively by your OS
- **Virtual Bluetooth testing**: Perform Bluetooth functional tests without physical hardware using virtual Bluetooth stacks like Android Emulator and Zephyr RTOS  
- **Cross-network connections**: Connect HCI Controllers that are not in the same radio network (virtual or physical)

## Installation

```bash
pip install -e git+https://github.com/vChavezB/bleak-bumble.git
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

## Documentation

- [Installation Guide](docs/installation.md)
- [Usage Instructions](docs/usage.md)  
- [Examples](docs/examples.md)
- [API Reference](docs/api.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

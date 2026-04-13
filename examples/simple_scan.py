#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Victor Chavez <vchavezb@protonmail.com>
"""
Simple example of using bleak_bumble to scan for BLE devices.

This example demonstrates how to use the Bumble backend with a TCP server transport.
"""

import asyncio
import logging
from bleak import BleakScanner
from bleak_bumble import BumbleTransportCfg, TransportScheme
from bleak_bumble.scanner import BleakScannerBumble

# Enable debug logging to see what's happening
logging.basicConfig(level=logging.INFO)


async def scan_for_devices():
    """Scan for BLE devices using the Bumble backend."""

    # Configure transport - TCP server on localhost port 1000
    cfg = BumbleTransportCfg(TransportScheme.TCP_SERVER, "127.0.0.1:1000")

    def detection_callback(device, advertisement_data):
        """Callback function called when a device is detected."""
        print(f"Found device: {device.name} ({device.address})")
        print(f"  RSSI: {advertisement_data.rssi}")
        print(f"  Service UUIDs: {advertisement_data.service_uuids}")
        print(f"  Manufacturer data: {advertisement_data.manufacturer_data}")
        print("---")

    # Create scanner with Bumble backend
    scanner = BleakScanner(
        detection_callback=detection_callback, 
        backend=BleakScannerBumble, 
        cfg=cfg
    )

    print("Starting BLE scan with Bumble backend...")
    print("Make sure you have a Bumble-compatible device or simulator running")
    print("that connects to TCP server on 127.0.0.1:1000")
    print()

    try:
        await scanner.start()
        print("Scanning for 10 seconds...")
        await asyncio.sleep(10.0)
    finally:
        await scanner.stop()
        print("Scan completed.")


if __name__ == "__main__":
    asyncio.run(scan_for_devices())

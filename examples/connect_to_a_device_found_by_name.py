#!/usr/bin/env python
"""
Simple example of using bleak_bumble to scan / connect.

This example demonstrates how to use Bumble backend with a transport.
Only very few modification is necessary to use this backend. 
"""

# Set environment variables.  This part can be outside of the code.
import os
# A virtual controller on TCP.
#os.environ["BLEAK_BUMBLE"] = "tcp_server:127.0.0.1:1000"
#
# An HCI H4 on serial port, should be detached from BT stack built in OS.
#os.environ["BLEAK_BUMBLE"] = "serial:/dev/ttyUSB0,1000000,rtscts"
#os.environ["BLEAK_BUMBLE_HOST"] = "1"
#
# The first HCI H2 on USB port, should be detached from BT stack built in OS.
# Appropriate firmware should be loaded before use with e.g. Realtek/Intel device.
# See official Google/Bumble docs for details. 
os.environ["BLEAK_BUMBLE"] = "usb:0"
os.environ["BLEAK_BUMBLE_HOST"] = "1"

import asyncio
from bleak import BleakScanner, BleakClient
from bleak_bumble.scanner import BleakScannerBumble
from bleak_bumble.client import BleakClientBumble

TARGET_NAME = 'NAME'

async def discover_device():
    async with BleakScanner(backend=BleakScannerBumble) as scanner:
        async def lookup_device():
            async for bd, ad in scanner.advertisement_data():
                print(f' {bd!r} with {ad!r}')
                if TARGET_NAME in (bd.name or '') or TARGET_NAME in (ad.local_name or ''):
                    return bd
        print("Scanning for Bluetooth devices...")
        try:
            device = await asyncio.wait_for(lookup_device(), timeout=30)
        except asyncio.TimeoutError:
            print('Target device not found.')
            return None
        print(f"Target device found : {device}")
        return device

async def main():
    device = await discover_device()
    if not device:
        return

    async with BleakClient(device, backend=BleakClientBumble) as client:
        if client.is_connected:
            print(f'Connected : {device}')

            # Do something here.
            await asyncio.sleep(5)

        else:
            print('Failed to connect to the target device.')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop() # Clear retained state.

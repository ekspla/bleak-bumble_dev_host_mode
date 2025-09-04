#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Victor Chavez <vchavezb@protonmail.com>

"""Tests for `bleak.backends.bumble` package, specifically scanning and advertising functionality."""

import asyncio
from asyncio import Queue
from typing import Tuple

import pytest
from bleak.backends.scanner import AdvertisementData, BLEDevice
from bumble.device import AdvertisingData, AdvertisingType

from bleak_bumble.scanner import BleakScannerBumble
from tests.test_utils import get_device, test_transport

ADV_PARAMS = {"name": "scan_dev", "addr": "12:34:56:78:AB:CD"}


@pytest.mark.asyncio
async def test_adv_data():
    """Test to validate that advertisement data can be detected correctly."""
    # Create a fresh queue for each test to avoid race conditions
    adv_data_queue: Queue[Tuple[BLEDevice, AdvertisementData]] = Queue()

    async def adv_cb(device: BLEDevice, data: AdvertisementData) -> None:
        """Callback to handle BLE device and advertisement data."""
        await adv_data_queue.put((device, data))

    scan_dev = get_device(ADV_PARAMS["addr"])
    adv_name_data = AdvertisingData(
        [(AdvertisingData.COMPLETE_LOCAL_NAME, ADV_PARAMS["name"].encode("utf-8"))]
    )

    await scan_dev.power_on()
    await scan_dev.start_advertising(
        advertising_type=AdvertisingType.UNDIRECTED,
        target=None,
        advertising_data=bytes(adv_name_data),
    )

    scanner = BleakScannerBumble(
        detection_callback=adv_cb,
        service_uuids=None,
        scanning_mode="active",
        cfg=test_transport,
    )

    await scanner.start()

    try:
        # Wait for a maximum of 3 seconds for an item from the queue
        device, data = await asyncio.wait_for(adv_data_queue.get(), timeout=3.0)

        assert device.name == ADV_PARAMS["name"]
        assert device.address == ADV_PARAMS["addr"]
    except asyncio.TimeoutError:
        pytest.fail("Test timed out waiting for advertisement data")
    finally:
        await scanner.stop()
        await scan_dev.stop_advertising()

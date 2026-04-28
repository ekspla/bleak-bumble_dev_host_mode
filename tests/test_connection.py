#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Victor Chavez <vchavezb@protonmail.com>

"""Tests for `bleak.backends.bumble` package, specifically connection functionality."""

import pytest
from bumble.gatt import Characteristic, Service
from bleak import BleakClient
from bleak.exc import BleakError
from bleak_bumble.client import BleakClientBumble
from tests.test_utils import get_device, test_transport

CONN_ADDR = "12:34:56:78:AB:CD"


@pytest.mark.asyncio
async def test_service():
    SVC_UUID = "50DB505C-8AC4-4738-8448-3B1D9CC09CC5"
    CHAR_UUID = "486F64C6-4B5F-4B3B-8AFF-EDE134A8446A"
    CHAR_VAL = "hello".encode()
    svc1 = Service(
        SVC_UUID,
        [
            Characteristic(
                CHAR_UUID,
                Characteristic.Properties.READ | Characteristic.Properties.NOTIFY,
                Characteristic.READABLE,
                CHAR_VAL,
            ),
        ],
    )
    conn_dev = get_device(CONN_ADDR)
    conn_dev.add_services([svc1])
    await conn_dev.power_on()
    await conn_dev.start_advertising()

    client = BleakClient(CONN_ADDR, backend=BleakClientBumble, cfg=test_transport)
    await client.connect()
    svc_found = False
    val = None
    for svc in (client_services := client.services):
        if svc.uuid == svc1.uuid:
            svc_found = True
            for char in svc.characteristics:
                if char.uuid == CHAR_UUID:
                    val = await client.read_gatt_char(char)
                    assert val == CHAR_VAL
                    break
    assert svc_found
    assert (await client._backend.get_services()) == client_services # Check cache.

    await client.disconnect()

    assert not client.is_connected
    mtu_size = start_notify = stop_notify = False
    try:
        client.mtu_size
    except BleakError:
        mtu_size = True
    assert mtu_size
    try:
        async def callback(char, data):
            pass
        await client.start_notify(CHAR_UUID, callback=callback)
    except BleakError:
        start_notify = True
    assert start_notify
    try:
        await client.stop_notify(CHAR_UUID)
    except BleakError:
        stop_notify = True
    assert stop_notify

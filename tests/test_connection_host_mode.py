#!/usr/bin/env python
"""Test for `bleak.backends.bumble` package, specifically connection with `host_mode`.

Although not of great importance, this test checks the `if host_mode==True:` branch.
"""
import asyncio
import pytest

from bumble.controller import Controller
from bumble.transport.common import Transport

from bleak import BleakClient
from bleak import BleakScanner

from bleak_bumble import transports, get_link
from bleak_bumble.client import BleakClientBumble
from bleak_bumble.scanner import BleakScannerBumble

from tests.test_utils import get_device

CONN_ADDR = "12:34:56:78:AB:CD"

@pytest.mark.asyncio
async def test_connect_host_mode():
    async def add_pytest_host_transport():
        """Connect the host to a virtual controller with LocalLink()."""
        if "pytest" in transports.keys():
            return transports["pytest"]
        controller = Controller(
            "client",
            link=get_link(),
        )
        transports["pytest"] = Transport(controller, controller)
        return transports["pytest"]

    conn_dev = get_device(CONN_ADDR)
    await conn_dev.power_on()
    await conn_dev.start_advertising()

    _ = await add_pytest_host_transport()

    device = await BleakScanner.find_device_by_name(
        conn_dev.name,
        backend=BleakScannerBumble,
        cfg="pytest",
        host_mode=True,
    )
    assert device is not None
    assert (transports.pop("pytest", None)) is None

    _ = await add_pytest_host_transport()

    client = BleakClient(
        device,
        backend=BleakClientBumble,
        cfg="pytest",
        host_mode=True,
    )

    await client.connect()
    await asyncio.sleep(1)
    assert client.is_connected

    await client.disconnect()
    assert (transports.pop("pytest", None)) is None

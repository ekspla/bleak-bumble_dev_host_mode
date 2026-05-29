#!/usr/bin/env python
"""Test for `bleak.backends.bumble` package, specifically connection with `host_mode`.

Although not of great importance, this test checks the `if host_mode==True:` branch.
"""

import asyncio

import pytest
from bleak import BleakClient, BleakScanner
from bumble.controller import Controller
from bumble.device import DeviceConfiguration
from bumble.hci import Address
from bumble.transport.common import Transport

from bleak_bumble import get_link, transports
from bleak_bumble.client import BleakClientBumble
from bleak_bumble.scanner import BleakScannerBumble
from tests.test_utils import get_device

CONN_ADDR = "12:34:56:78:AB:CD"


@pytest.mark.asyncio
@pytest.mark.parametrize("use_dev_config", [False, True])
async def test_connect_host_mode(use_dev_config: bool):
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

    kwargs = {"cfg": "pytest", "host_mode": True}
    if use_dev_config:
        kwargs["dev_cfg"] = DeviceConfiguration(
            name="pytest", address=Address("F0:F1:F2:F3:F4:F5")
        )

    device = await BleakScanner.find_device_by_name(
        conn_dev.name,
        backend=BleakScannerBumble,
        **kwargs,
    )

    assert device is not None
    assert (transports.pop("pytest", None)) is None

    _ = await add_pytest_host_transport()

    client = BleakClient(
        device,
        backend=BleakClientBumble,
        **kwargs,
    )

    await client.connect()
    assert client.is_connected

    await client.disconnect()
    assert (transports.pop("pytest", None)) is None

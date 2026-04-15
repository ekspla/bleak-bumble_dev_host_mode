"""Modified version of a test in `bleak.tests.integration`"""

import asyncio
import pytest
from typing import TYPE_CHECKING

from bumble.device import Device

from bleak import BleakClient
from bleak_bumble.client import BleakClientBumble

from tests.conftest import (
    configure_and_power_on_bumble_peripheral,
    find_ble_device,
)

@pytest.mark.asyncio
@pytest.mark.skipif(
    True,
    reason="HCI_READ_RSSI_COMMAND is not supported on virtual controller with LocalLink(), use a physical controller.", 
)
async def test_get_rssi(bumble_peripheral: Device):
    """Getting RSSI from client is possible."""
    await configure_and_power_on_bumble_peripheral(bumble_peripheral)

    device = await find_ble_device(bumble_peripheral)

    async with BleakClient(device, backend=BleakClientBumble) as client:

        backend = client._backend  # pyright: ignore[reportPrivateUsage]
        rssi = await backend._connection.get_rssi()
        # Verify that this value is an integer and not some other
        # type from a ffi binding framework.
        assert isinstance(rssi, int)

        # The rssi can vary. So we only check for a plausible range.
        assert -127 <= rssi < 0

@pytest.mark.asyncio
async def test_mtu_size(bumble_peripheral: Device):
    """Check if the mtu size can be optained."""
    await configure_and_power_on_bumble_peripheral(bumble_peripheral)

    device = await find_ble_device(bumble_peripheral)

    async with BleakClient(device, backend=BleakClientBumble) as client:
        mtu_size = client.mtu_size

        # Verify that this value is an integer and not some other
        # type from a ffi binding framework.
        assert isinstance(mtu_size, int)

        # The mtu_size is different between different platforms. So we only check
        # for a plausible range.
        assert 23 <= mtu_size <= 517

"""Modified version of a test in `bleak.tests.integration`"""

import asyncio

import pytest
from bleak import BleakClient
from bleak.backends import BleakBackend, get_default_backend
from bumble.device import Device

from bleak_bumble.client import BleakClientBumble
from tests.conftest import (
    configure_and_power_on_bumble_peripheral,
    find_ble_device,
)


@pytest.mark.asyncio
@pytest.mark.skipif(
    True,
    reason="this test is used on CoreBluetooth but not on Bumble",
)
async def test_pairing_unavailable(bumble_peripheral: Device):
    """Check if pairing on CoreBluetooth raises an error."""
    await configure_and_power_on_bumble_peripheral(bumble_peripheral)

    device = await find_ble_device(bumble_peripheral)

    client = BleakClient(device, backend=BleakClientBumble)
    with pytest.raises(NotImplementedError):
        await client.pair()
    with pytest.raises(NotImplementedError):
        await client.unpair()


# TODO: Add tests for pairing

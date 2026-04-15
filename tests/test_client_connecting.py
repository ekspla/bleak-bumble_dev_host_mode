"""Modified version of a test in `bleak.tests.integration`"""

import asyncio
import pytest

from bumble.device import Device

from bleak import BleakClient
from bleak._compat import timeout as async_timeout
from bleak_bumble.client import BleakClientBumble

from tests.conftest import (
    configure_and_power_on_bumble_peripheral,
    find_ble_device,
)

@pytest.mark.asyncio
async def test_connect(bumble_peripheral: Device):
    """Connecting to a BLE device is possible."""
    await configure_and_power_on_bumble_peripheral(bumble_peripheral)

    device = await find_ble_device(bumble_peripheral)

    async with BleakClient(device, backend=BleakClientBumble) as client:
        assert client.name == bumble_peripheral.name

@pytest.mark.asyncio
async def test_connect_multiple_times(bumble_peripheral: Device):
    """Connecting to a BLE device multiple times is possible."""
    await configure_and_power_on_bumble_peripheral(bumble_peripheral)

    device = await find_ble_device(bumble_peripheral)

    async with BleakClient(device, backend=BleakClientBumble):
        pass

    await bumble_peripheral.start_advertising()

    async with BleakClient(device, backend=BleakClientBumble):
        pass

@pytest.mark.asyncio
async def test_is_connected(bumble_peripheral: Device):
    """Check if a connection is connected is working."""
    await configure_and_power_on_bumble_peripheral(bumble_peripheral)

    device = await find_ble_device(bumble_peripheral)

    client = BleakClient(device, backend=BleakClientBumble)

    assert client.is_connected is False
    async with BleakClient(device, backend=BleakClientBumble) as client:
        assert client.is_connected is True
    assert client.is_connected is False

@pytest.mark.asyncio
async def test_disconnect_callback(bumble_peripheral: Device):
    """Check if disconnect callback is called."""
    await configure_and_power_on_bumble_peripheral(bumble_peripheral)

    device = await find_ble_device(bumble_peripheral)

    disconnected_client_future: asyncio.Future[BleakClient] = asyncio.Future()

    def disconnected_callback(client: BleakClient):
        disconnected_client_future.set_result(client)

    async with BleakClient(device, disconnected_callback, backend=BleakClientBumble) as client:
        # Disconnect from virtual device side
        virtual_connection = list(bumble_peripheral.connections.values())[0]
        await virtual_connection.disconnect()

        # Wait for disconnected callback to be called
        async with async_timeout(5):
            disconnected_client = await disconnected_client_future
        assert disconnected_client is client

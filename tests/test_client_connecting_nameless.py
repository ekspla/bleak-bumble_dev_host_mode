"""This is simulating an unusual nameless peripheral which does not advertise name and which lacks gap service."""

import asyncio

import pytest
from bleak import BleakClient
from bumble import data_types
from bumble.controller import Controller
from bumble.core import AdvertisingData
from bumble.device import Device, DeviceConfiguration
from bumble.hci import Address
from bumble.host import Host

from bleak_bumble import get_link
from bleak_bumble.client import BleakClientBumble


@pytest.mark.asyncio
async def test_connect_nameless_device():

    # use random static address to avoid device caching issues, when characteristics change between test runs
    address = Address.generate_static_address()
    device = Device(
        name=None,
        address=address,
        config=DeviceConfiguration(gap_service_enabled=False),
    )
    device.name = None  # This is necessary because `name` defaults to 'Bumble'.
    adv_data = [
        data_types.Flags(
            AdvertisingData.Flags.LE_GENERAL_DISCOVERABLE_MODE
            | AdvertisingData.Flags.BR_EDR_NOT_SUPPORTED
        ),
    ]
    device.host = Host()
    device.host.controller = Controller("dev", link=get_link())
    await device.power_on()
    await device.start_advertising(advertising_data=bytes(AdvertisingData(adv_data)))

    bd = address.to_string(with_type_qualifier=False)

    async with BleakClient(bd, backend=BleakClientBumble) as client:
        assert client.name == bd.replace(":", "-")

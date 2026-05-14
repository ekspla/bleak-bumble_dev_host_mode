"""Tests for `bleak.backends.bumble` package, specifically `Just Works` pairing."""

import pytest
from bleak import BleakClient
from bumble.gatt import Characteristic, Service

from bleak_bumble.client import BleakClientBumble
from tests.test_utils import get_device, test_transport

CONN_ADDR = "F1:F2:F3:F4:F5:F6"
HEART_RATE_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"


# Suppress warning from Session.start_encryption() in `bumble/smp.py`
@pytest.mark.filterwarnings("ignore::DeprecationWarning:bumble.*")
@pytest.mark.asyncio
async def test_just_works_pairing():
    conn_dev = get_device(CONN_ADDR)
    svc = Service(
        HEART_RATE_SERVICE,
        [
            Characteristic(
                HEART_RATE_MEASUREMENT,
                Characteristic.Properties.READ,
                Characteristic.READ_REQUIRES_AUTHENTICATION,
                bytes(1),
            ),
        ],
    )
    conn_dev.add_services([svc])
    await conn_dev.power_on()
    await conn_dev.start_advertising()

    async with BleakClient(
        CONN_ADDR, backend=BleakClientBumble, cfg=test_transport
    ) as client:
        hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
        with pytest.raises(Exception):
            val = await client.read_gatt_char(hrm_char)

    await conn_dev.start_advertising()

    async with BleakClient(
        CONN_ADDR, backend=BleakClientBumble, cfg=test_transport
    ) as client:
        await client.pair()
        hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
        val = await client.read_gatt_char(hrm_char)
        assert bytes(val) == bytes(1)

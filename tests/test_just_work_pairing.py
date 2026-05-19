"""Tests for `bleak.backends.bumble` package, specifically `Just Work` pairing."""

import asyncio

import pytest
from bleak import BleakClient
from bumble.device import DeviceConfiguration
from bumble.gatt import Characteristic, Service

from bleak_bumble.client import BleakClientBumble
from tests.test_utils import get_device, test_transport

CONN_ADDR = "F1:F1:F1:F1:F1:F1"
CLIENT_BD_ADDR = "F0:F1:F2:F3:F4:F5"
HEART_RATE_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"

SVC = Service(
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


# Suppress warning from Session.start_encryption() in `bumble/smp.py`
@pytest.mark.filterwarnings("ignore::DeprecationWarning:bumble.*")
@pytest.mark.asyncio
async def test_just_work_pairing():
    conn_dev = get_device(CONN_ADDR)
    conn_dev.add_services([SVC])
    await conn_dev.power_on()
    await conn_dev.start_advertising(auto_restart=True)

    # Without a key in MemoryKeyStore, no pairing
    # --> should fail to read.
    async with BleakClient(
        CONN_ADDR, backend=BleakClientBumble, cfg=test_transport
    ) as client:
        hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
        with pytest.raises(Exception):
            val = await client.read_gatt_char(hrm_char)

    # Pair
    # --> should update a key in the keystore and should succeed to read.
    async with BleakClient(
        CONN_ADDR, backend=BleakClientBumble, cfg=test_transport
    ) as client:
        await client.pair()
        hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
        val = await client.read_gatt_char(hrm_char)
        assert bytes(val) == bytes(1)


# Suppress warning from Session.start_encryption() in `bumble/smp.py`
@pytest.mark.filterwarnings("ignore::DeprecationWarning:bumble.*")
@pytest.mark.asyncio
async def test_bonding_unpairing():
    conn_dev = get_device(CONN_ADDR)
    conn_dev.add_services([SVC])
    await conn_dev.power_on()
    await conn_dev.start_advertising(auto_restart=True)

    dev_cfg = DeviceConfiguration.from_dict(
        {"name": "client", "address": CLIENT_BD_ADDR, "keystore": "JsonKeyStore"}
    )

    # With JsonKeyStore, pair
    # --> should update a key in the keystore and should succeed to read.
    async with BleakClient(
        CONN_ADDR, backend=BleakClientBumble, cfg=test_transport, dev_cfg=dev_cfg
    ) as client:
        hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
        await client.pair()
        val = await client.read_gatt_char(hrm_char)
        assert bytes(val) == bytes(1)

    # With the key in keysore, encrypt
    # --> should succeed to read.
    # Unpair
    # --> delete the key from keystore.
    async with BleakClient(
        CONN_ADDR, backend=BleakClientBumble, cfg=test_transport, dev_cfg=dev_cfg
    ) as client:
        hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
        await client._backend._connection.encrypt()
        val = await client.read_gatt_char(hrm_char)
        assert bytes(val) == bytes(1)

        await client.unpair()
        key = await client._backend._dev.keystore.get(CONN_ADDR)
        assert key is None
        await client.unpair()

    # Without a key in the keystore (unpaired), encrypt
    # --> should fail to encrypt.
    async with BleakClient(
        CONN_ADDR, backend=BleakClientBumble, cfg=test_transport, dev_cfg=dev_cfg
    ) as client:
        hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
        with pytest.raises(Exception):
            await asyncio.wait_for(client._backend._connection.encrypt(), timeout=2)
            val = await client.read_gatt_char(hrm_char)

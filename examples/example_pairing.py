#!/usr/bin/env python
"""An example of how to pair/bond with a peripheral using various I/O capabilties:
'keyboard', 'display', 'display+keyboard', 'display+yes/no' and 'none'.

`Delegate` in `bumble/apps/pair.py` is used for ease of demonstration. 

It was tested against `bumble/apps/pair.py` peripheral on Linux
by changing combinations of initiator's and responder's I/Os.
"""

import asyncio
import click
from functools import wraps

from bumble.apps.pair import Delegate  # Use Delegate in apps for ease of demonstrations. 
from bumble.device import DeviceConfiguration
from bumble.pairing import PairingConfig

from bleak import BleakClient, BleakScanner
from bleak_bumble.client import BleakClientBumble
from bleak_bumble.scanner import BleakScannerBumble


CLIENT_BD_ADDR = "F0:F1:F2:F3:F4:F5"

# Reading this characteristics requires pairing.
HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"

SC = True  # True: Secure Connections protocol / False: Legacy protocol
MITM = True  # Request MITM protection
BONDING = True  # Enable bonding
MODE = "le"
PROMPT = False  # Prompt to accept/reject pairing request


def async_cmd(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@click.command()
@click.option(
    '--io',
    type=click.Choice(
        ['keyboard', 'display', 'display+keyboard', 'display+yes/no', 'none']
    ),
    default='none',  # 'none' for Just Works pairing
    show_default=True,
)
@click.argument('hci_transport')
@async_cmd
async def main(io, hci_transport):
    dev_cfg = DeviceConfiguration.from_dict(
        {
            "name": "client",
            "address": CLIENT_BD_ADDR,
            "keystore": "JsonKeyStore",
            "irk": "865F81FF5A8B486EAAE29A27AD9F77DC",
        }
    )

    target_device = await BleakScanner.find_device_by_name(
        "Bumble", backend=BleakScannerBumble, cfg=hci_transport, host_mode=True, dev_cfg=dev_cfg
    )

    print("Connecting...")
    async with BleakClient(
        target_device, backend=BleakClientBumble, cfg=hci_transport, host_mode=True, dev_cfg=dev_cfg
    ) as client:

        print('Connected.')
        await asyncio.sleep(1)

        # This should fail.
        try:
            hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
            val = await client.read_gatt_char(hrm_char)
            print(f"Heart rate: {val}")
        except:
            print("Failed to read without pairing.")
    print("Disconnected.\n")

    await asyncio.sleep(2)

    print("Connecting...")
    async with BleakClient(
        target_device, backend=BleakClientBumble, cfg=hci_transport, host_mode=True, dev_cfg=dev_cfg
    ) as client:

        print('Connected.')
        await asyncio.sleep(1)

        # Use Delegate in bumble/apps/pair.py
        backend = client._backend
        backend._dev.pairing_config_factory = lambda connection: PairingConfig(
            sc=SC,
            mitm=MITM,
            bonding=BONDING,
            #oob=oob_contexts,
            #identity_address_type=identity_address_type,
            delegate=Delegate(MODE, connection, io, PROMPT),
        )

        print("Pairing...")
        await client.pair()

        # This should succeed.
        try:
            hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
            val = await client.read_gatt_char(hrm_char)
            print(f"Heart rate: {val}")
        except:
            print("Failed to read.")
    print("Disconnected.\n")

    await asyncio.sleep(2)

    print("Connecting...")
    async with BleakClient(
        target_device, backend=BleakClientBumble, cfg=hci_transport, host_mode=True, dev_cfg=dev_cfg
    ) as client:

        print('Connected.')
        await asyncio.sleep(1)

        # Use Delegate in bumble/apps/pair.py
        backend = client._backend
        backend._dev.pairing_config_factory = lambda connection: PairingConfig(
            sc=SC,
            mitm=MITM,
            bonding=BONDING,
            #oob=oob_contexts,
            #identity_address_type=identity_address_type,
            delegate=Delegate(MODE, connection, io, PROMPT),
        )

        print("Encrypt using the key in keystore...")
        await client._backend._connection.encrypt()

        # This should succeed.
        try:
            hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
            val = await client.read_gatt_char(hrm_char)
            print(f"Heart rate: {val}")
        except:
            print("Failed to read.")

        print("Unpairing...")
        await client.unpair()
        key = await client._backend._dev.keystore.get(target_device.address)
        assert key is None
        print("Unpaired: the key was deleted.")
    print("Disconnected.\n")

    await asyncio.sleep(2)

    print("Connecting...")
    async with BleakClient(
        target_device, backend=BleakClientBumble, cfg=hci_transport, host_mode=True, dev_cfg=dev_cfg
    ) as client:

        print('Connected.')
        await asyncio.sleep(1)

        # Use Delegate in bumble/apps/pair.py
        backend = client._backend
        backend._dev.pairing_config_factory = lambda connection: PairingConfig(
            sc=SC,
            mitm=MITM,
            bonding=BONDING,
            #oob=oob_contexts,
            #identity_address_type=identity_address_type,
            delegate=Delegate(MODE, connection, io, PROMPT),
        )

        key = await client._backend._dev.keystore.get(target_device.address)
        assert key is None
        print("The key does not exist.")

        # This should fail.
        print("Try to encrypt without the key in keystore...")
        try:
            await client._backend._connection.encrypt()
        except:
            print("Failed to encrypt without the key.")
    print("Disconnected")


if __name__ == "__main__":
    main()

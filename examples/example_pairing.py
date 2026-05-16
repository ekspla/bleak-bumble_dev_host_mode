"""This example demonstrates how to pair with a peripheral with various IOs:
'keyboard', 'display', 'display+keyboard', 'display+yes/no' and 'none'.

`Delegate` in `bumble/apps/pair.py` is used for ease of demonstration. 

It was tested against `bumble/apps/pair.py` peripheral on Linux
by changing combinations of initiator's and responder's IOs.
"""

import asyncio
import click
from functools import wraps

from bumble.apps.pair import Delegate  # Use Delegate in apps for ease of demonstrations. 
from bumble.hci import Address
from bumble.pairing import PairingConfig

from bleak import BleakClient, BleakScanner
from bleak_bumble.client import BleakClientBumble
from bleak_bumble.scanner import BleakScannerBumble


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
    target_device = await BleakScanner.find_device_by_name(
        "Bumble", backend=BleakScannerBumble, cfg=hci_transport, host_mode=True
    )

    print("Connecting...")
    async with BleakClient(
        target_device, backend=BleakClientBumble, cfg=hci_transport, host_mode=True
    ) as client:

        print('Connected.')
        await asyncio.sleep(1)

        # This should fail.
        try:
            hrm_char = client.services.get_characteristic(HEART_RATE_MEASUREMENT)
            val = await client.read_gatt_char(hrm_char)
            print(f"Heart rate: {val}")
        except:
            print("Failed to read.")
    print("Disconnected")

    await asyncio.sleep(2)

    async with BleakClient(
        target_device, backend=BleakClientBumble, cfg=hci_transport, host_mode=True
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
        await client.disconnect()
    print("Disconnected")


if __name__ == "__main__":
    main()

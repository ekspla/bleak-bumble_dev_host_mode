"""This example demonstrates receiving LE extended advertisements with scanner.

It was tested with a pair of RTL8761B usb dongles on Linux, 
and was confirmed to work by using nRF BLE sniffer.
"""

import asyncio

from bumble import data_types
from bumble.core import AdvertisingData
from bumble.device import Device, AdvertisingParameters
from bumble.hci import Address, HCI_LE_1M_PHY, HCI_LE_2M_PHY, HCI_LE_CODED_PHY

from bleak import BleakScanner
from bleak_bumble import start_transport
from bleak_bumble.scanner import BleakScannerBumble


async def main():
    transport = await start_transport("usb:0", True)
    bumble_peripheral = Device.with_hci(
        name="Bumble",
        #address=Address.generate_static_address(),
        address=Address('F1:F2:F3:F4:F5:F6'),
        hci_source=transport.source,
        hci_sink=transport.sink,
    )
    adv_data = [
        data_types.Flags(
            AdvertisingData.Flags.LE_GENERAL_DISCOVERABLE_MODE
            | AdvertisingData.Flags.BR_EDR_NOT_SUPPORTED
        ),
        data_types.CompleteLocalName(bumble_peripheral.name),
        # An appropriate/long test data.
        data_types.ManufacturerSpecificData(128, bytes(
            "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.0123456789"
            "the quick brown fox jumps over the lazy dog.0123456789",
            "utf8"
            )
        ),
    ]
    await bumble_peripheral.power_on()
    advertising_set = await bumble_peripheral.create_advertising_set(
        advertising_parameters = AdvertisingParameters(
            primary_advertising_interval_min = 200,
            primary_advertising_interval_max = 200,
            primary_advertising_phy = HCI_LE_1M_PHY,
            secondary_advertising_phy = HCI_LE_CODED_PHY,
            secondary_advertising_phy_options = 0,
        ),
        advertising_data = bytes(AdvertisingData(adv_data)),
        #auto_start = False,
        auto_start = True,
        #auto_restart = False,
        auto_restart = True,
    )

    #await advertising_set.start()
    async with BleakScanner(backend=BleakScannerBumble, cfg="usb:1", host_mode=True) as scanner:
        async def scanning():
            async for bd, ad in scanner.advertisement_data():
                print(f' {bd!r} with {ad!r}')
        try:
            await asyncio.wait_for(scanning(), timeout=5)
        except asyncio.TimeoutError:
            pass

    #await asyncio.sleep(10)
    #await advertising_set.stop()

    await bumble_peripheral.power_off()
    await transport.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop() # Clear retained state.

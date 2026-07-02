#!/usr/bin/env python
"""This example using a pair of controllers demonstrates LE extended advertisement.

Bleak-Bumble scanner with RTL8761B dongle was successful in receiving extended 
advertisements (LE_CODED_PHY S=2/S=8, LE_1M_PHY) sent from another RTL8761B as 
well as from Zephyr's HCI-USB on nRF52840. The advertisement packets were 
confirmed by nRF BLE sniffer in both cases.

NOTES:
 - My RTL8761B controllers always prefer S=2 in LE_CODED advertisement broadcast. 
   This is in contrast to the explanation in Bluetooth specification as follows:
   `If advertising on the LE Coded PHY, the S=8 coding shall be assumed.`

 - A Zephyr's HCI-USB nRF52840 dongle used as a broadcaster always prefers S=8 
   in LE_CODED advertisement, in agreement with the Bluetooth spec.

 - Coding Scheme Selection on Advertising (CSSA), which allows to specify the 
   coding parameter `S`, is introduced in Bluetooth 5.4. RTL8761C probably works.

 - `HCI_LE_Set_Extended_Advertising_Parameters_V2_Command` for CSSA is not yet 
   supoorted in Bumble==0.0.230.
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
        data_types.ManufacturerSpecificData(65535, bytes(
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
            primary_advertising_phy = HCI_LE_CODED_PHY,
            secondary_advertising_phy = HCI_LE_CODED_PHY,
            # The following options are ignored unless 
            # HCI_LE_SET_EXTENDED_ADVERTISING_PARAMETERS_V2 
            # is supported by both the controller and the host (Bumble).
            #primary_advertising_phy_options = 4,
            #secondary_advertising_phy_options = 4,
        ),
        advertising_data = bytes(AdvertisingData(adv_data)),
        #auto_start = False,
        auto_start = True,
        #auto_restart = False,
        auto_restart = True,
    )

    #await advertising_set.start()
    async with BleakScanner(
        scanning_mode="passive", backend=BleakScannerBumble, cfg="usb:1", host_mode=True
    ) as scanner:
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

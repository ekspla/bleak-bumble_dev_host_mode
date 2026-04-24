"""This example demonstrates how to get/set connection PHYs.

It was tested with a pair of RTL8761B usb dongles on Linux, 
and was confirmed to work by using nRF BLE sniffer.
"""

import asyncio

from bumble import data_types
from bumble.core import AdvertisingData
from bumble.device import Device, AdvertisingParameters
from bumble.hci import Address, HCI_LE_1M_PHY, HCI_LE_2M_PHY, HCI_LE_CODED_PHY

from bleak import BleakClient
from bleak import BleakScanner
from bleak_bumble import start_transport
from bleak_bumble.client import BleakClientBumble
from bleak_bumble.scanner import BleakScannerBumble

# True: LE extendend advertising ('1m', 'coded') / False: LE legacy advertising ('1m').
LE_EXTENDED_ADV = True

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
    ]
    await bumble_peripheral.power_on()
    
    if not LE_EXTENDED_ADV:
        bumble_peripheral.advertising_interval_min = bumble_peripheral.advertising_interval_max = 200
        bumble_peripheral.advertising_data = bytes(AdvertisingData(adv_data))
        await bumble_peripheral.start_advertising()

    else:
        advertising_set = await bumble_peripheral.create_advertising_set(
            advertising_parameters = AdvertisingParameters(
                primary_advertising_interval_min = 200,
                primary_advertising_interval_max = 200,
                primary_advertising_phy = HCI_LE_1M_PHY,
                secondary_advertising_phy = HCI_LE_CODED_PHY,
                secondary_advertising_phy_options = 0,
            ),
            advertising_data = bytes(AdvertisingData(adv_data)),
        )

    #await asyncio.sleep(10)

    device = await BleakScanner.find_device_by_name(
        bumble_peripheral.name,
        backend=BleakScannerBumble,
        cfg="usb:1",
        host_mode=True,
    )
    async with BleakClient(
        device,
        backend=BleakClientBumble,
        cfg="usb:1",
        host_mode=True,
        phys="1m,2m,coded",
    ) as client:
        if client.is_connected:
            print('Connected.')
            backend = client._backend
            print(f'phys: {backend._phys}')
            #print(f'preferences: {backend._connection_parameters_preferences}')
            phy1 = await backend._connection.get_phy()
            print(phy1)

            await backend._connection.set_phy(
                tx_phys=[HCI_LE_CODED_PHY],
                rx_phys=[HCI_LE_CODED_PHY],
                phy_options=0,
            )
            await asyncio.sleep(1)
            phy2 = await backend._connection.get_phy()
            print(phy2)

            await backend._connection.set_phy(
                tx_phys=[HCI_LE_2M_PHY],
                rx_phys=[HCI_LE_2M_PHY],
            )
            await asyncio.sleep(1)
            phy3 = await backend._connection.get_phy()
            print(phy3)

            await backend._connection.set_phy(
                tx_phys=[HCI_LE_1M_PHY],
                rx_phys=[HCI_LE_1M_PHY],
            )
            await asyncio.sleep(1)
            phy4 = await backend._connection.get_phy()
            print(phy4)
        else:
            print('Failed.')
        print('Disconnecting...')
    await bumble_peripheral.power_off()
    await transport.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop() # Clear retained state.

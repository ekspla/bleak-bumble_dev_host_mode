"""This example demonstrates how to change connection PHY.

It was tested with a pair of RTL8761B usb dongles on Linux, 
and was confirmed to work by using nRF BLE sniffer.
"""

import asyncio

from bumble import data_types
from bumble.core import AdvertisingData, DataType
from bumble.device import Device
from bumble.hci import Address, Phy, HCI_LE_1M_PHY, HCI_LE_2M_PHY, HCI_LE_CODED_PHY

from bleak import BleakClient
from bleak import BleakScanner
from bleak._compat import timeout as async_timeout
from bleak_bumble import start_transport
from bleak_bumble.client import BleakClientBumble
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
    bumble_peripheral.advertising_interval_min = bumble_peripheral.advertising_interval_max = 200
    adv_data = [
        data_types.Flags(
            AdvertisingData.Flags.LE_GENERAL_DISCOVERABLE_MODE
            | AdvertisingData.Flags.BR_EDR_NOT_SUPPORTED
        ),
        data_types.CompleteLocalName(bumble_peripheral.name),
    ]
    bumble_peripheral.advertising_data = bytes(AdvertisingData(adv_data))
    await bumble_peripheral.power_on()
    await bumble_peripheral.start_advertising()
    
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

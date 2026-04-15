"""Modified version of conftest in `bleak.tests.integration`"""

import pytest
from bumble import data_types
from bumble.core import AdvertisingData, DataType
from bumble.controller import Controller
from bumble.device import Device
from bumble.gatt import Service
from bumble.hci import Address
from bumble.host import Host

from bleak import BleakScanner
from bleak.backends.device import BLEDevice

from bleak_bumble import get_link
from bleak_bumble.scanner import BleakScannerBumble


@pytest.fixture
def bumble_peripheral() -> Device:
    """
    Create a BLE peripheral device with bumble.
    """
    device = Device(
        name="Bleak",
        # use random static address to avoid device caching issues, when characteristics change between test runs
        address=Address.generate_static_address(),
    )
    return device


def add_default_advertising_data(
    bumble_peripheral: Device,
    additional_adv_data: list[DataType] | None = None,
) -> None:
    """Add default advertising data to bumble peripheral."""
    adv_data: list[DataType] = [
        data_types.Flags(
            AdvertisingData.Flags.LE_GENERAL_DISCOVERABLE_MODE
            | AdvertisingData.Flags.BR_EDR_NOT_SUPPORTED
        ),
        data_types.CompleteLocalName(bumble_peripheral.name),
    ]
    if additional_adv_data:
        adv_data.extend(additional_adv_data)
    bumble_peripheral.advertising_data = bytes(AdvertisingData(adv_data))


async def configure_and_power_on_bumble_peripheral(
    bumble_peripheral: Device,
    additional_adv_data: list[DataType] | None = None,
    services: list[Service] | None = None,
) -> None:
    """Configure and power on the bumble peripheral."""
    add_default_advertising_data(bumble_peripheral, additional_adv_data)
    if services:
        bumble_peripheral.add_services(services)
    bumble_peripheral.host = Host()
    bumble_peripheral.host.controller = Controller("dev", link=get_link())
    await bumble_peripheral.power_on()
    await bumble_peripheral.start_advertising()


async def find_ble_device(bumble_peripheral: Device) -> BLEDevice:
    """Find the BLE device corresponding to the bumble peripheral."""
    device = await BleakScanner.find_device_by_name(bumble_peripheral.name, backend=BleakScannerBumble)
    if device is None:
        raise RuntimeError("failed to discover device, is Bumble working?")

    return device

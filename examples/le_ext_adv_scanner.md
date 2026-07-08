# An example of BLE5 extended advertisement scanner with Bleak-Bumble

## Using a RTL8761B as scanner and an another RTL8761B or Zephyr HCI-USB as advertiser

**Bleak-Bumble scanner / observer successfully worked with RTL8761B dongle** 
(UB500, TP-Link, with fw 0xddd5c761) **in receiving extended advertisements (LE_1M_PHY and 
LE_CODED_PHY S=2 / S=8)** sent from Bumble advertiser / broadcaster.  

``` bash
python examples/le_ext_adv_scanner.py
 ...

 BLEDevice(F1:F2:F3:F4:F5:F6, Bumble) with AdvertisementData(local_name='Bumble', manufacturer_data={65535: b'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.0123456789the quick brown fox jumps over the lazy dog.0123456789'}, tx_power=127, rssi=-12)

 ...
```

Because Coding Scheme Selection on Advertising (CSSA) introduced in Bluetooth 5.4, 
which allows to specify the coding parameter `S`, is not supported in Bumble host 
and in my bluetooth controllers yet, two different controllers have to be used for 
`S=2` and `S=8` in LE_CODED_PHY; RTL8761B (another UB500) was used for [`S=2`](figs/ext_adv_S2.jpg) coding while 
[Zephyr's HCI-USB](https://docs.zephyrproject.org/latest/samples/bluetooth/hci_usb/README.html) 
\(Xiao nRF52840\) for [`S=8`](figs/ext_adv_S8.jpg). In all of the cases, **advertisement packets were 
[confirmed](figs/le_ext_adv_wireshark.md) by nRF BLE sniffer** (Nordic's nRF52840 dongle) with Wireshark.  

| Scanner/Observer | Advertiser/Broadcaster | PHY         | Result |
| ---------------- | ---------------------- | ----------- | ------ |
| RTL8761B         | RTL8761B               | 1M          | works  |
| RTL8761B         | RTL8761B               | CODED (S=2) | works  |
| RTL8761B         | RTL8761B               | CODED (S=8) | -      |
| RTL8761B         | Zephyr HCI-USB         | 1M          | works  |
| RTL8761B         | Zephyr HCI-USB         | CODED (S=2) | -      |
| RTL8761B         | Zephyr HCI-USB         | CODED (S=8) | works  |

## Notes:  

 - Because CSSA is introduced in Bluetooth 5.4, the latest dongles ~~such as 
   RTL8761C~~ may work.

 - A RTL8761CUV dongle has been bought and tested, only to fail in using LE_CODED_PHY. 
   Receiving extended advertisements in LE_1M_PHY/LE_2M_PHY and changing from 1M to 2M and 
   v.v. during connection worked perfectly though. I was not aware that *RTL8761C lacks 
   LE_CODED functionality* before I saw the datasheet.

 - `HCI_LE_Set_Extended_Advertising_Parameters_V2_Command` for CSSA is not yet 
   fully supoorted in Bumble (as of 0.0.230).

 -  Zephyr's HCI-USB firmware was built for my Xiao nRF52840 (with bootloader) 
    by using Zephyr-RTOS (v4.4) and Zephyr-SDK (v1.0) as follows:

``` bash
west build -p always -b nrf52840dongle samples/bluetooth/hci_usb \
 -DCONFIG_FLASH_LOAD_OFFSET=0x1000\
 -DCONFIG_BUILD_OUTPUT_HEX=y\
 -DCONFIG_BT_EXT_ADV=y\
 -DCONFIG_BT_EXT_ADV_LEGACY_SUPPORT=y\
 -DCONFIG_BT_EXT_ADV_MAX_ADV_SET=2\
 -DCONFIG_BT_CTLR_ADV_EXT=y\
 -DCONFIG_BT_CTLR_ADV_DATA_LEN_MAX=191\
 -DCONFIG_BT_CTLR_SCAN_DATA_LEN_MAX=191\
 -DCONFIG_BT_BUF_ACL_RX_SIZE=502\
 -DCONFIG_BT_BUF_ACL_TX_SIZE=502\
 -DCONFIG_BT_CTLR_DATA_LENGTH_MAX=251\
 -DCONFIG_BT_DATA_LEN_UPDATE=y\
 -DCONFIG_BT_CTLR_ADVANCED_FEATURES=y\
 -DCONFIG_BT_CTLR_CONN_RSSI=y\
 -DCONFIG_BT_CTLR_TX_PWR_DYNAMIC_CONTROL=y
```  

 - Although Xiao is cheap, easily available and convenient for a quick test like 
   this, I do not recommend to use it in real BLE5 applications because of its 
   poor antenna.

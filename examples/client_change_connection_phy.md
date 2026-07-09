# An example of BLE 5 to demonstrate how to get/set connection PHYs with Bleak-Bumble

## Using Bleak-Bumble with an RTL8761B dongle as scanner/client and Bumble with another RTL8761B dongle as advertiser/peripheral

**Bleak-Bumble client successfully worked with RTL8761B dongle** (UB500, TP-Link, with fw 0xddd5c761) 
**in using LE_1M_PHY, LE_2M_PHY and LE_CODED_PHY (S=2/S=8)** during connections. In all of the cases, 
the packets were confirmed by nRF BLE sniffer (Nordic's nRF52840 dongle) with Wireshark.

``` bash
python examples/client_change_connection_phy.py
Connected.
phys: [<Phy.LE_1M: 1>, <Phy.LE_2M: 2>, <Phy.LE_CODED: 3>]
ConnectionPHY(tx_phy=<Phy.LE_CODED: 3>, rx_phy=<Phy.LE_CODED: 3>)    # See note below.
ConnectionPHY(tx_phy=<Phy.LE_CODED: 3>, rx_phy=<Phy.LE_CODED: 3>)
ConnectionPHY(tx_phy=<Phy.LE_2M: 2>, rx_phy=<Phy.LE_2M: 2>)
ConnectionPHY(tx_phy=<Phy.LE_1M: 1>, rx_phy=<Phy.LE_1M: 1>)
Disconnecting...
```

## Notes  

 - Connection always starts with secondary advertising PHY if extended advertisement is used. 
   In this example, the primary and secondary PHYs were LE_1M_PHY and LE_CODED_PHY, respectively.

 - Optionally use `phy_options` (defaults to `0`: no preference) for coding scheme in LE_CODED_PHY.

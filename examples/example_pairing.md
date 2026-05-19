# An example of pairing/bonding with delegate built-in Bumble for various combinations of initiator's and responder's I/O capabilities

## Usage example with two virtual controllers  
Can be also run on two real/physical controllers, of course.  

- On the first console, run **virtual controllers**  
`tnt0`--`tnt1` and `tnt2`--`tnt3`, in this case, were paired virtual null modem cables using [tty0tty](https://github.com/freemed/tty0tty). 
On Windows, use [com0com](https://com0com.sourceforge.net/). 
```
python lib/python3.12/site-packages/bumble/apps/controllers.py \
serial:/dev/tnt1,1000000,rtscts \
serial:/dev/tnt3,1000000,rtscts
```

- On the second console, run **peripheral** example stored in `bumble/apps`.  
The I/O defaults to 'display+keyboard'.
```
python lib/python3.12/site-packages/bumble/apps/pair.py \
lib/python3.12/site-packages/bumble/examples/device3.json \
serial:/dev/tnt0,1000000,rtscts
```

- On the third console, run this **central** example stored in `bleak_bumble/examples`.  
The I/O ['keyboard', 'display', 'display+keyboard', 'display+yes/no', 'none'] defaults to 'none'.
```
python example_pairing.py \
"serial:/dev/tnt2,1000000,rtscts" \
--io 'display'
```

## Console output on peripheral (Bumble) side: `io='display+keyboard'`
```Shell
<<< Connection: Connection(transport=LE, handle=0x0001, role=PERIPHERAL, self_address=F1:F2:F3:F4:F5:F6, self_resolvable_address=None, peer_address=F0:F1:F2:F3:F4:F5, peer_resolvable_address=None)
<<< Connection: Connection(transport=LE, handle=0x0001, role=PERIPHERAL, self_address=F1:F2:F3:F4:F5:F6, self_resolvable_address=None, peer_address=F0:F1:F2:F3:F4:F5, peer_resolvable_address=None)
***-----------------------------------
*** Pairing starting
***-----------------------------------
###-----------------------------------
### Pairing with client [F0:F1:F2:F3:F4:F5]
###-----------------------------------
>>> Enter PIN: 254644
@@@-----------------------------------
@@@ Connection is encrypted
@@@-----------------------------------
***-----------------------------------
*** Paired! (peer identity=F0:F1:F2:F3:F4:F5)
*** address_type: 1
*** ltk:
***   value: 1e99699dce7ae132f6446bf4d3f8ecc0
***   authenticated: True
*** irk:
***   value: 865f81ff5a8b486eaae29a27ad9f77dc
***   authenticated: True
***-----------------------------------
<<< Connection: Connection(transport=LE, handle=0x0001, role=PERIPHERAL, self_address=F1:F2:F3:F4:F5:F6, self_resolvable_address=None, peer_address=F0:F1:F2:F3:F4:F5, peer_resolvable_address=None)
@@@-----------------------------------
@@@ Connection is encrypted
@@@-----------------------------------
<<< Connection: Connection(transport=LE, handle=0x0001, role=PERIPHERAL, self_address=F1:F2:F3:F4:F5:F6, self_resolvable_address=None, peer_address=F0:F1:F2:F3:F4:F5, peer_resolvable_address=None)
```

## Console output on central (Bleak-Bumble) side: `io='display'`
```Shell
Connecting...
Connected.
!!! unexpected error while reading characteristics: AUTHENTICATION_FAILURE_ERROR
Failed to read without pairing.
Disconnected.

Connecting...
Connected.
Pairing...
###-----------------------------------
### Pairing with Bumble3 [F1:F2:F3:F4:F5:F6]
### PIN: 254644
###-----------------------------------
Heart rate: bytearray(b'\x00')
Disconnected.

Connecting...
Connected.
Encrypt using the key in keystore...
Heart rate: bytearray(b'\x00')
Unpairing...
Unpaired: the key was deleted.
Disconnected.

Connecting...
Connected.
The key does not exist.
Try to encrypt without the key in keystore...
Failed to encrypt without the key.
Disconnected
```

#!/usr/bin/env python3

import lan9514
import time
import struct
import sys
import sign_eeprom

EEPROM_SIZE = 512

board_rev = "C02"
serial = sys.argv[1]

eeprom_base = lan9514.Lan9514(
    manufacturer_id = "X1Plus",
    product_name = f"Expander X1P-002-{board_rev}",
    serial_number = f"X1P-002-{board_rev}-{serial}",
    hs_device_descriptor = b'\x12\x01\x00\x02\x00\x00\x00\x40\x24\x04\x00\xec\x00\x01\x01\x02\x03\x01',
    fs_device_descriptor = b'\x12\x01\x00\x02\x00\x00\x00\x40\x24\x04\x00\xec\x00\x01\x01\x02\x03\x01',
    #hs_config_descriptor = b"\t\x02'\x00\x01\x01\x00\xe0\x01\t\x04\x00\x00\x03\xff\x00\xff\x00",
    #fs_config_descriptor = b"\t\x02'\x00\x01\x01\x00\xe0\x01\t\x04\x00\x00\x03\xff\x00\xff\x00",
).encode()

# tail data format:
#   last byte is a single version number
#   packet of known length is prepended to that
#
#   version 1: 4 bytes
#     4 bytes: time_t serialization_date
#
#   version 2: 68 bytes
#     64 bytes: ECDSA signature
#     4 bytes: time_t serialization_date

eeprom = sign_eeprom.sign(eeprom_base + b'\xFF' * (EEPROM_SIZE - len(eeprom_base)))

fname = f"eeprom-X1P-002-{board_rev}-{serial}.bin"
with open(fname, 'wb') as f:
    f.write(eeprom)

print(f"write with: ./ethtool -E eth0 magic 0x9500 offset 0 length 512 < {fname}")

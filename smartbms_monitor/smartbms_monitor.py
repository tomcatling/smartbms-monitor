#!/usr/bin/python

import serial
import binascii
import struct

# port = serial.Serial(
#     "/dev/ttyS0", 
#     parity=serial.PARITY_NONE, 
#     stopbits=serial.STOPBITS_ONE,
#     baudrate=9600, 
#     timeout=3.0
# )

# while True:
#     rcv = port.read()
#     print(rcv)



bytemap = {
    "total_voltage": {"type":'number',"bytes":[0,1,2],"scale":0.005,"offset":0,"unit":"V"},
    "sign_I1": {"type":'character',"bytes":[3]},
    "current_I1": {"type":'number',"bytes":[4,5],"scale":0.125,"offset":0,"unit":"A"},
    "sign_I2": {"type":'character',"bytes":[6]},
    "current_I2": {"type":'number',"bytes":[7,8],"scale":0.125,"offset":0,"unit":"A"},
    "sign_I3": {"type":'character',"bytes":[9]},
    "current_I3": {"type":'number',"bytes":[10,11],"scale":0.125,"offset":0,"unit":"A"},
    "Vmin": {"type":'number',"bytes":[12,13],"scale":0.005,"offset":0,"unit":"V"},
    "Vmin_cell_number": {"type":'number',"bytes":[14],"scale":1,"offset":0,"unit":None},
    "Vmax": {"type":'number',"bytes":[15,16],"scale":0.005,"offset":0,"unit":"V"},
    "Vmax_cell_number": {"type":'number',"bytes":[17],"scale":1,"offset":0,"unit":None},
    "Tmin": {"type":'number',"bytes":[18,19],"scale":1,"offset":-276.0,"unit":"K"},
    "Tmin_cell_number": {"type":'number',"bytes":[20],"scale":1,"offset":0,"unit":None},
}


def gen_checksum(packet):
    chck = 0
    for b in packet:
        chck += int(b)
    return chck & 0xFF # lowest 8 bits

def check_checksum(packet):
    checksum = packet[-1]
    return checksum == gen_checksum(packet[:-1])


def print_packet(packet):
    for b in packet:
        print(hex(b))


packet = bytearray(b'\x01\x05\xFF\x2B\x01\x00\x2B\x01\x00\x2B\x01\x00\x02\x30\x32\x02\x30\x32\x01\x14\x32')
packet.append(gen_checksum(packet))

assert check_checksum(packet)

for item, properties in bytemap.items():
    print(item, end=': ')
    start = properties['bytes'][0]
    end = properties['bytes'][-1]
    if len(properties['bytes']) == 3:
        num = struct.unpack(">L", b'\x00'+packet[start:end+1])[0]
    if len(properties['bytes']) == 2:
        num = struct.unpack(">H", packet[start:end+1])[0]
    if len(properties['bytes']) == 1:
        num = struct.unpack(">H", b'\x00'+packet[start:end+1])[0]

    if properties['type'] == 'character':
        print(chr(num))
    else:
        print(num*properties['scale'] + properties['offset'])
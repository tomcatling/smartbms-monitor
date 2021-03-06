import binascii
import struct
import sys

bytemap = {
    "battery_voltage": {"type":'number',"bytes":[0,1,2],"scale":0.005,"offset":0,"unit":"V"},
    "charge_current_sign": {"type":'character',"bytes":[3]},
    "charge_current": {"type":'number',"bytes":[4,5],"scale":0.125,"offset":0,"unit":"A"},
    "load_current_sign": {"type":'character',"bytes":[6]},
    "load_current": {"type":'number',"bytes":[7,8],"scale":0.125,"offset":0,"unit":"A"},
    "battery_current_sign": {"type":'character',"bytes":[9]},
    "battery_current": {"type":'number',"bytes":[10,11],"scale":0.125,"offset":0,"unit":"A"},
    "Vmin": {"type":'number',"bytes":[12,13],"scale":0.005,"offset":0,"unit":"V"},
    "Vmin_cell_number": {"type":'number',"bytes":[14],"scale":1,"offset":0},
    "Vmax": {"type":'number',"bytes":[15,16],"scale":0.005,"offset":0,"unit":"V"},
    "Vmax_cell_number": {"type":'number',"bytes":[17],"scale":1,"offset":0},
    "Tmin": {"type":'number',"bytes":[18,19],"scale":1,"offset":-276.0,"unit":"K"},
    "Tmin_cell_number": {"type":'number',"bytes":[20],"scale":1,"offset":0},
    "Tmax": {"type":'number',"bytes":[21,22],"scale":1,"offset":-276.0,"unit":"K"},
    "Tmax_cell_number": {"type":'number',"bytes":[23],"scale":1,"offset":0},
    "this_cell_number": {"type":'number',"bytes":[24],"scale":1,"offset":0},
    "number_of_cells": {"type":'number',"bytes":[25],"scale":1,"offset":0},
    "this_cell_voltage": {"type":'number',"bytes":[26,27],"scale":0.005,"offset":0,"unit":"V"},
    "this_cell_temp": {"type":'number',"bytes":[28,29],"scale":1,"offset":-276.0,"unit":"K"},
    "status_byte": {"type":'status',"bytes":[30]},
    "energy_collected_today": {"type":'number',"bytes":[31,32,33],"scale":0.001,"offset":0,"unit":"kWh"},
    "energy_stored": {"type":'number',"bytes":[34,35,36],"scale":0.001,"offset":0,"unit":"kWh"},
    "energy_consumed_today": {"type":'number',"bytes":[37,38,39],"scale":0.001,"offset":0,"unit":"kWh"},
    "state_of_charge": {"type":'number',"bytes":[40],"scale":1,"offset":0},
    "total_energy_colleted": {"type":'number',"bytes":[41,42,43],"scale":0.001,"offset":0,"unit":"kWh"},
    "total_energy_consumed": {"type":'number',"bytes":[44,45,46],"scale":0.001,"offset":0,"unit":"kWh"},
    "device_hours": {"type":'number',"bytes":[47],"scale":1,"offset":0,"unit":"h"},
    "device_minutes": {"type":'number',"bytes":[48],"scale":1,"offset":0,"unit":"m"},
    "battery_capacity": {"type":'number',"bytes":[49,50],"scale":0.1,"offset":0,"unit":"kWh"},
    "configured_Vmin": {"type":'number',"bytes":[51,52],"scale":0.005,"offset":0,"unit":"V"},
    "configured_Vmax": {"type":'number',"bytes":[53,54],"scale":0.005,"offset":0,"unit":"V"},
    "configured_Vbalance": {"type":'number',"bytes":[55,56],"scale":0.005,"offset":0,"unit":"V"},
}

def gen_checksum(packet):
    """
    Create a checksum for the given packet.
    """
    chck = 0
    for b in packet:
        chck += int(b)
    return chck & 0xFF # lowest 8 bits

def check_checksum(packet):
    """
    Check that the checksum attached to the packet
    matches what we would expect.
    """
    checksum = packet[-1]
    if all([int(i)==0 for i in packet]):
        return False
    elif all([int(i)==255 for i in packet]):
        return False
    else:
        return checksum == gen_checksum(packet[:-1])


def print_packet(packet):
    """
    Print out a packet for debugging.
    """
    print('')
    for b in packet:
        sys.stdout.write(hex(b))
    print('')

def decode(packet):
    """
    Decode a packet using the bytemap. This returns
    a dictionary of properties and values.
    """

    output = {}

    for item, properties in bytemap.items():
        start = properties['bytes'][0]
        end = properties['bytes'][-1]
        if len(properties['bytes']) == 3:
            num = struct.unpack(">L", b'\x00'+packet[start:end+1])[0]
        if len(properties['bytes']) == 2:
            num = struct.unpack(">H", packet[start:end+1])[0]
        if len(properties['bytes']) == 1:
            num = struct.unpack(">H", b'\x00'+packet[start:end+1])[0]

        if properties['type'] == 'character':
            output.update({item:chr(num)})
        elif properties['type'] == 'number':
            output.update({item:num*properties['scale'] + properties['offset']})

    return output

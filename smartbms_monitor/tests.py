
import utils

test_packet = bytearray(
    b'\x01\x05\xFF' # total voltage
    +b'\x2B' # I1 sign
    +b'\x01\x00' # I1
    +b'\x2B' # I2 sign
    +b'\x01\x00' # I2
    +b'\x2B' # I3 sign
    +b'\x01\x00' # I3 
    +b'\x02\x30' # Vmin
    +b'\x32' # Vmin cell number
    +b'\x02\x30' # Vmax 
    +b'\x32' # Vmax cell number
    +b'\x01\x14' # Tmin 
    +b'\x32' # Tmin cell number
    +b'\x01\x28' # Tmax
    +b'\x32' # Tmax cell number
    +b'\x32' # cell number
    +b'\xFF' # number of cells
    +b'\x02\x30' # cell voltage
    +b'\x01\x28' # cell temp 
    +b'\x03' # status
    +b'\x00\x00\x64' # today energy collected
    +b'\x00\xF2\x21' # energy stored
    +b'\x00\x00\x64' # today energy consumed
    +b'\x32' # status
    +b'\x64\x00\x00' # total energy collected
    +b'\x64\x00\x00' # total energy consumed
    +b'\x16' # device hours
    +b'\x20' # device minutes
    +b'\x00\xA0' # battery capacity
    +b'\x15\xFF' # Vmin setting
    +b'\x15\xFF' # Vmax setting
    +b'\x15\xFF' # Vbypass setting
    )

def test_checksum():
    """
    Check that the checksum logic is self-consistent.
    """
    packet_to_test = test_packet[:]
    packet_to_test.append(
        utils.gen_checksum(packet_to_test)
    )
    
    try:
        assert utils.check_checksum(packet_to_test)
    except AssertionError:
        print("Checksum logic failed")
        exit(1)
    else:
        print("Checksum OK")


expected_output = {
    'total_voltage': 335.355, 
    'I1_sign': '+', 
    'I1': 32.0, 
    'I2_sign': '+', 
    'I2': 32.0, 
    'I3_sign': '+', 
    'I3': 32.0, 
    'Vmin': 2.8000000000000003, 
    'Vmin_cell_number': 50, 
    'Vmax': 2.8000000000000003, 
    'Vmax_cell_number': 50, 
    'Tmin': 0.0, 
    'Tmin_cell_number': 50, 
    'Tmax': 20.0, 'Tmax_cell_number': 50, 
    'info_cell_number': 50, 
    'number_of_cells': 255, 
    'cell_voltage': 2.8000000000000003, 
    'cell_temp': 20.0, 
    'today_energy_colleted': 0.1, 
    'energy_stored': 61.985, 
    'today_energy_consumed': 0.1, 
    'state_of_charge': 50, 
    'total_energy_colleted': 6553.6, 
    'total_energy_consumed': 6553.6, 
    'device_hours': 22, 
    'device_minutes': 32, 
    'battery_capacity': 16.0, 
    'Vmin_setting': 28.155, 
    'Vmax_setting': 28.155, 
    'Vbypass_setting': 28.155
}

def test_decode():
    """
    Check that decoding the test packet creates
    the expected output.
    """
    packet_to_test = test_packet[:]
    packet_to_test.append(
        utils.gen_checksum(packet_to_test)
    )

    try:
        assert utils.decode(packet_to_test) == expected_output
    except AssertionError:
        print("Decode logic failed")
        exit(1)
    else:
        print("Decode OK")

if __name__ == "__main__":
    test_checksum()
    test_decode()
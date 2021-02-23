import serial

from utils import decode, check_checksum, print_packet

port = serial.Serial(
    "/dev/ttyS0", 
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE,
    baudrate=9600, 
    timeout=3.0
)

while True:
    b = port.read()
    print(b)

while True:
    # wait for start bit
    while port.read() == b'\x00':
        pass
    rcv = bytearray(port.read(58))
    print(check_checksum(rcv))
    print_packet(rcv)
    #output = decode(rcv)
    #print(output['state_of_charge'])


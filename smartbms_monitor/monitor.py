import serial

from utils import decode 

port = serial.Serial(
    "/dev/ttyS0", 
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE,
    baudrate=9600, 
    timeout=3.0
)



while True:    

    # wait for start bit
    while port.read() != b'\x01':
        pass

    rcv = bytearray(b'')
    while len(rcv) < 58:
        rcv.append(port.read())

    output = decode(rcv)

    print(output)


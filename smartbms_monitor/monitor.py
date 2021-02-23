import serial
from smartbms_monitor.utils import decode, check_checksum, print_packet

port = serial.Serial(
    "/dev/ttyS0", 
    parity=serial.PARITY_NONE, 
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    baudrate=9600, 
    timeout=1,
    xonxoff = 0,
    rtscts = 0,
    dsrdtr = 0
)
port.reset_input_buffer()

cell_voltages = {}

while True:
    # wait for start bit
    buffer = []
    while all([b==255 for b in buffer]):
        buffer = [ord(port.read(1))^0xff for i in range(10)]
        pass
    rcv = bytearray(buffer)
    while len(rcv) < 70:
        rcv.append((ord(port.read(1)) ^ 0xff))   
    # cut 58 indices back from zero at the end 
    while rcv[-1] == 255:
        _=rcv.pop()
    rcv = rcv[-58:]
    rcv = bytearray([i>>1 for i in rcv])
    if check_checksum(rcv):

        output = decode(rcv)

        cell_voltages[output['info_cell_number']] = output['cell_voltage']
        stage_of_charge = output['state_of_charge']

        print(cell_voltages)
        print(stage_of_charge)
        
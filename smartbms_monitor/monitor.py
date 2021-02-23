import serial
import boto3
import time
from smartbms_monitor.utils import decode, check_checksum, print_packet

client = boto3.client('timestream-write')
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

        cell_voltage = output['cell_voltage']+0.635
        stage_of_charge = output['state_of_charge']
        total_voltage = output['total_voltage']+0.635
        time_in_seconds = time.time()

        print(output['info_cell_number'])
        print(cell_voltage)
        print(total_voltage)
        print(stage_of_charge)
        
        response = client.write_records(
            DatabaseName='BroadBeanBMS',
            TableName='StatusUpdates',
            Records=[
                {
                    'MeasureName': 'TotalVoltage',
                    'MeasureValue': str(total_voltage),
                    'MeasureValueType': 'DOUBLE',
                    'Time': str(time_in_seconds),
                    'TimeUnit': 'SECONDS',
                    'Version': 123
                },
                {
                    'Dimensions': [
                        {
                            'Name': 'CellNumber',
                            'Value': str(output['info_cell_number']),
                            'DimensionValueType': 'VARCHAR'
                        },
                    ],
                    'MeasureName': 'CellVoltage',
                    'MeasureValue': str(cell_voltage),
                    'MeasureValueType': 'DOUBLE',
                    'Time': str(time_in_seconds),
                    'TimeUnit': 'SECONDS',
                    'Version': 123
                },
                {
                    'MeasureName': 'StateOfCharge',
                    'MeasureValue': str(stage_of_charge),
                    'MeasureValueType': 'DOUBLE',
                    'Time': str(time_in_seconds),
                    'TimeUnit': 'SECONDS',
                    'Version': 123
                },
            ]
        )

        time.sleep(1)
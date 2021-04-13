import serial
import boto3
import json
import os
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
i=0

while True:
    # wait for start bit
    rcv = bytearray(port.read(58))
    if check_checksum(rcv):
        output = decode(rcv)
        dimensions = []
        for k,v in output.items():
            # print(str(k) + ':  ' + str(v))
            dimensions.append({
                'Name':k,
                'Value':str(v),
            })

        response = client.write_records(
            DatabaseName='BroadBeanBMS',
            TableName='StatusUpdates',
            Records=[
                {
                    'Dimensions': dimensions,
                    'MeasureName': 'StatusUpdate',
                    'MeasureValue': str(rcv[-1]),
                    'MeasureValueType': 'BIGINT',
                    'Time': str(int(time.time())),
                    'TimeUnit': 'SECONDS',
                }
            ]
        )
        i+=1
        if i%100==0:
            with open(os.environ['HOME']+'/bms_status.json','w') as f:
                f.write(json.dumps(output))

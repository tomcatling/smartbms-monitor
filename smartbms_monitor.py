#!/usr/bin/python

import serial
from data_map import data_map

port = serial.Serial(
    "/dev/ttyS0", 
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE,
    baudrate=9600, 
    timeout=3.0
)

while True:
    rcv = port.read()
    print(rcv)

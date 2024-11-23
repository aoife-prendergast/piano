import sys
import time

import pyvisa as visa
import serial.tools.list_ports as port_list
import serial
import numpy as np

def view_ports():
    ports = list(port_list.comports())
    for p in ports:
        print(p)

view_ports()
serialcomm = serial.Serial("COM5",115200)

serialcomm.timeout = 0.5

addr = 777


# For Piano

init = False
read_ID = True
data_out = True
general_test = False
gpio_3 = 0

if init:
    query = str(f"ADDR:{addr}:ADC:MEAS:BITS 1.0 (@{1})\n ")
    serialcomm.write(query.encode())
    time.sleep(1)
    data_read = serialcomm.read(serialcomm.in_waiting)
    # print("Primary Side:")
    print(data_read.strip())

if read_ID:
    query = str(f"ADDR:{addr}:ADC:MEAS:VOLT? (@{1})\n ")
    serialcomm.write(query.encode())
    time.sleep(0.010)
    data_read = serialcomm.read(serialcomm.in_waiting)
    # print("Primary Side:")
    print(data_read.strip())

if data_out:
    query = str(f"ADDR:{addr}:ADC:MEAS:BYTE 16 (@{1})\n ")
    serialcomm.write(query.encode())
    time.sleep(0.5)
    data_read = serialcomm.read(serialcomm.in_waiting)
    # print("Primary Side:")
    print(data_read.strip())


if general_test:
    query = str(f"ADDR:{addr}:ADC:MEAS:VOLT 1.0 (@{1})\n ")
    serialcomm.write(query.encode())
    time.sleep(2)
    data_read = serialcomm.read(serialcomm.in_waiting)
    # print("Primary Side:")
    print(data_read.strip())

if gpio_3 == 1:
    query = str(f"ADDR:{addr}:ADC:MEAS:LEVEL 1.0 (@{1})\n ")
    serialcomm.write(query.encode())
    print("GPIO3 On")

if gpio_3 == 2:
    query = str(f"ADDR:{addr}:ADC:MEAS:LEVEL 1.0 (@{0})\n ")
    serialcomm.write(query.encode())
    print("GPIO3 Off")



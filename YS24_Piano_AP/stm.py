import serial 
import serial.tools.list_ports

print(list(serial.tools.list_ports.comports()))

import glob
import time

"""
"/dev/ttyS0"
leftSTMComm = serial.Serial("/dev/ttyS0",baudrate=115200,)
#self.rightSTMComm = serial.Serial('COM5',baudrate=115200,)

query = str(f"ADDR:777:ADC:MEAS:VOLT? 1.0 (@6)\n")

#read left STM values
leftSTMComm.write(query.encode())
leftReturn = leftSTMComm.read()

print(leftReturn)
"""

temp_list = glob.glob ('/dev/tty[A-Za-z]*')

result = []
for a_port in temp_list:

    try:
        s = serial.Serial(a_port)
        s.close()
        result.append(a_port)
    except serial.SerialException:
        pass

print(result)

leftSTMComm = serial.Serial("/dev/ttyACM0",baudrate=115200,)
#self.rightSTMComm = serial.Serial('COM5',baudrate=115200,)

query = str(f"ADDR:777:ADC:MEAS:VOLT? 1.0 (@6)\n")

#read left STM values
leftSTMComm.write(query.encode())
time.sleep(0.005)
leftReturn = leftSTMComm.read(leftSTMComm.in_waiting)

print(leftReturn)
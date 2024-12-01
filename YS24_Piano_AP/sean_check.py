import serial
import time
import glob

leftSTMComm = serial.Serial("/dev/ttyACM1",baudrate=115200,)

def idn():
    query = str(f"ADDR:777:*IDN?\n")

    #read left STM values
    leftSTMComm.write(query.encode())
    time.sleep(0.2)
    leftReturn = leftSTMComm.read(leftSTMComm.in_waiting)
    print(leftReturn)

def init():
    query = str(f"ADDR:777:ADC:MEAS:BITS 1.0 (@0)\n")

    #read left STM values
    leftSTMComm.write(query.encode())
    time.sleep(0.5)
    leftReturn = leftSTMComm.read(leftSTMComm.in_waiting)
    print(leftReturn)

def read_reg():
    query = str(f"ADDR:777:ADC:MEAS:VOLT? 1.0 (@0)\n")

    #read left STM values
    leftSTMComm.write(query.encode())
    time.sleep(0.05)
    leftReturn = leftSTMComm.read(leftSTMComm.in_waiting)
    print(leftReturn)

def calibrate():
    query = str(f"ADDR:777:ADC:MEAS:TEMP 1.0 (@0)\n")

    #read left STM values
    leftSTMComm.write(query.encode())
    time.sleep(0.2)
    leftReturn = leftSTMComm.read(leftSTMComm.in_waiting)
    print(leftReturn)

def reset_adc():
    query = str(f"ADDR:777:ADC:MEAS:LEVEL 1.0 (@0)\n")

    #read left STM values
    leftSTMComm.write(query.encode())
    time.sleep(0.2)
    leftReturn = leftSTMComm.read(leftSTMComm.in_waiting)
    print(leftReturn)


def get_key_presses():
    query = str(f"ADDR:777:ADC:MEAS:CURR 1.0 (@0)\n")

    #read left STM values
    leftSTMComm.write(query.encode())
    time.sleep(0.008)
    leftReturn = leftSTMComm.read(leftSTMComm.in_waiting)

    print(leftReturn)
    list = str(leftReturn).replace("b","")
    list = list.replace("'","")
    combined = list.split(",")
    print(combined)

# temp_list = glob.glob ('/dev/tty[A-Za-z]*')

# result = []
# for a_port in temp_list:

#     try:
#         s = serial.Serial(a_port)
#         s.close()
#         result.append(a_port)
#     except serial.SerialException:
#         pass

# print(result)
# idn()
# time.sleep(1)

reset_adc()
time.sleep(1)
init()

calibrate()
time.sleep(1)

read_reg()
enabled = False

print("Looping all keys")
if enabled:
    while True:
        get_key_presses()
        time.sleep(0.05)
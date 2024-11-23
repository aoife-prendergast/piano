import AD4115_SPI_Driver as adc_spi
from AD4115_SPI_Driver import register_map
from time import sleep
import time
import matplotlib.pyplot as plt
import numpy as np
import spidev

import RPi.GPIO as GPIO
import time

#from pydub import AudioSegment
#from pydub.playback import play, _play_with_simpleaudio

#-----------------------------------------------------------------------
# GPIO and Sound Setup

# start = AudioSegment.from_wav("/home/strimble/Documents/GIT/TheVaultBTYSE/Audio/3-2-1_GO.wav")
# mission_impossible = AudioSegment.from_mp3("/home/strimble/Documents/GIT/TheVaultBTYSE/Audio/Mission Impossible Themefull theme.mp3")

#------------------------------------------------------------------------
# SPI and ADC Setup
class ADC: 
    def __init__(self): 
        self.spi = adc_spi.spi_open()

    def adc_setup(self):
        adc_spi.write_adc(self.spi,register_map['ADCMODE'],0x8600)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['IFMODE'],0x1040)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['GPIOCON'],0x2880)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['SETUPCON0'],0x420)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH0'],0x8010)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH1'],0x8030)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH2'],0x8050)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH3'],0x8070)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH4'],0x8090)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH5'],0x80B0)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH6'],0x80D0)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH7'],0x80F0)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH8'],0x8110)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH9'],0x8130)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH10'],0x8150)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH11'],0x8170)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH12'],0x0)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH13'],0x0)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH14'],0x0)
        sleep(0.1)
        adc_spi.write_adc(self.spi,register_map['CH15'],0x0)
        sleep(0.1)

        response = adc_spi.read_adc(self.spi,register_map['ID'])

        byte0 = '{0:08b}'.format(response[1])
        byte1 = '{0:08b}'.format(response[2])
        byte2 = '{0:08b}'.format(response[3])

        if hex(int(str(byte0+byte1),2)) == "0x38de":
            print("Comms Connected")
            return True
        else:
            print("Comms Failed")
            return False

    def adc_read(self):
        key_trigger = [0]*12
        on_threshold = 300000
        for i in range (12):
            adc_spi.GPIO3_LO(self.spi)
            adc_spi.GPIO3_HI(self.spi)
            adc_spi.GPIO3_LO(self.spi)
            sleep(0.001)
            response = adc_spi.read_adc(self.spi,register_map['DATA'])

            byte0 = '{0:08b}'.format(response[1])
            byte1 = '{0:08b}'.format(response[2])
            byte2 = '{0:08b}'.format(response[3])
            val = int(str(byte0+byte1+byte0),2)

            if response[4] < 12: #check if a valid channel
                if val < on_threshold:
                    key_trigger[response[4]] = 0
                else:
                    key_trigger[response[4]] = 1

        #print(key_trigger)
        return key_trigger

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  piano_key.py
#  
#  Copyright 2023  <piano@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from gpiozero import *
import time
import threading
from threading import Thread 
import mido

from pydub import AudioSegment

from adafruit_led_animation import helper
from adafruit_led_animation.color import *
import board
import neopixel
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.sequence import AnimationSequence
import serial.tools.list_ports
import digitalio
from pixel_mapping import PianoPixelMap
import serial
import glob
"""
global pixel_pin
global pixel_num 
global pixels
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  piano_key.py
#  
#  Optimized Version

import time
import threading
import mido
import serial
import glob

from adafruit_led_animation.color import RED
from adafruit_led_animation.animation.solid import Solid
from pydub import AudioSegment
from pixel_mapping import PianoPixelMap


class SerialPortManager:
    @staticmethod
    def find_ports():
        """Discover available serial ports."""
        ports = glob.glob('/dev/tty[A-Za-z]*')
        valid_ports = []
        for port in ports:
            try:
                with serial.Serial(port) as s:
                    valid_ports.append(port)
            except serial.SerialException:
                pass
        return valid_ports

    @staticmethod
    def initialize_port(port_path, baudrate=115200):
        """Initialize a serial port."""
        return serial.Serial(port_path, baudrate=baudrate)

class ADCInterface:
    @staticmethod
    def send_command(comport, command, delay=0.05):
        query = f"ADDR:777:ADC:MEAS:{command} 1.0 (@0)\n".encode()
        comport.write(query)
        time.sleep(delay)
        return comport.read(comport.in_waiting).decode().strip()

    @staticmethod
    def initialize(comport):
        return ADCInterface.send_command(comport, "BITS",0.5)

    @staticmethod
    def calibrate(comport):
        return ADCInterface.send_command(comport, "TEMP", 0.2)

    @staticmethod
    def reset_adc(comport):
        return ADCInterface.send_command(comport, "LEVEL",0.2)

    @staticmethod
    def read_register(comport):
        return ADCInterface.send_command(comport, "VOLT?",0.05)

    @staticmethod
    def read_adc(comport):
        return ADCInterface.send_command(comport, "CURR", 0.012)

    @staticmethod
    def adc_full_init(comport):
        initialised = False

        registers = ADCInterface.read_register(comport)
        if ('38 de' in registers) and ('80 0' in registers) and ('10 40' in registers) and ('28 0' in registers):
            initialised = True
            print('ADC Already Initialised')

        while not initialised:
            ADCInterface.reset_adc(comport)
            time.sleep(2)
            ADCInterface.initialize(comport)
            time.sleep(1)
            registers = ADCInterface.read_register(comport)
            if ('38 de' in registers) and ('80 0' in registers) and ('10 40' in registers) and ('28 0' in registers):
                initialised = True
                print('ADC Initialised')
            else:
                print('Failed to program ADC')
                print(registers)

        ADCInterface.calibrate(comport)

midioutPort = mido.open_output('xyz:xyz 129:0')

class Piano: 
    def __init__(self): 
        self.noOfKeys = 0
        self.noOfNotes = 0
        self.soundType = "piano"
        # key list
        self.keys = []
        self.notes = []
        self.combined = [0] * 24

        self.exit = False

        """
        port = mido.open_input('abc', virtual=True)
        print(mido.get_output_names())
        """

        midioutPort = mido.open_output('xyz:xyz 129:0')
        
        # Serial setup
        available_ports = SerialPortManager.find_ports()
        print("Available Ports:", available_ports)
        self.leftSTMComm = SerialPortManager.initialize_port("/dev/ttyACM0")
        self.rightSTMComm = SerialPortManager.initialize_port("/dev/ttyACM1")

        ADCInterface.adc_full_init(self.leftSTMComm)
        ADCInterface.adc_full_init(self.rightSTMComm)


    def addKey(self, key):
        self.keys.append(key)
        self.noOfKeys += 1

    def addNotes(self, notes):
        self.notes = self.notes + notes
        self.noOfNotes = len(self.notes)
        
    def resetLights(self):
        print("Setting all key unactive colors")
        for key in self.keys:
            key.setUnactiveState()

    def calibrate_ADCs(self): 
        ADCInterface.calibrate(self.leftSTMComm)
        ADCInterface.calibrate(self.rightSTMComm)

    def loop_LEDs(self):
        #used for self play - parse midi song
        print("thread started")
        
        while not self.exit:
            for key in self.keys:
                if key.getLEDState() != key.getState():
                    if key.getState() == 1:
                        key.led_on()
                        #print('SAM')
                    else: 
                        # print("turning off LED")
                        key.led_off()
                        #print('AOIFE')
                        #key.counter = 0
            time.sleep(0.05)

    def exit_loop(self):
        input('Press to exit')
        self.exit = True

    def loopKeys(self, active):
        print("Looping all keys")
        # for key in self.keys: 
        #     key.makeActive()
        self.exit = False
        threading.Thread(target=self.exit_loop, daemon=True).start()

        while not self.exit:
            leftReturn = ADCInterface.read_adc(self.leftSTMComm)
            rightReturn = ADCInterface.read_adc(self.rightSTMComm)

            #only continue if both ports returned something of a certain length (at least twelve 0/1s seperated by commas)
            if (len(leftReturn) >= 23) and (len(rightReturn) >= 23): 
                self.combined = (leftReturn + "," + rightReturn).split(",")
                #print(self.combined)

                for val, key in enumerate(self.keys):
                    if key.getState() != int(self.combined[val]):
                        #print(key.getState())
                        #print(int(combined[val]))
                        #there has been a state change
                        if int(self.combined[val]) == 1:
                            key.notePressed()
                        else: 
                            key.noteReleased()
            time.sleep(0.05)
        

                    
    def countKeys(self):
        return self.noOfKeys
            
    def reset(self):
        self.noOfKeys = 0
        self.soundType = "piano"
        self.keys = []

    def setScale(self, scale_select): 
        
        if (scale_select >= 1) and (scale_select <= 6):
            scale_select -= 1
            scale_select = scale_select*12
            for key in self.keys:
                print(scale_select)
                key.setNote(self.notes[scale_select])
                scale_select+=1
        else: 
            print("Invalid Scale Input")

    def parseSongMidi(self, midiSong):

        threading.Thread(target=self.loop_LEDs, daemon=True).start()

        self.exit = False
        threading.Thread(target=self.exit_loop, daemon=True).start()

        mid = mido.MidiFile(midiSong)
        
        # find scale
        max = 0
        for msg in mid:
            if(msg.type in ['note_on','note_off']):
                
                if msg.note > max :
                    max = msg.note
                    
        
        print(max)
        scale = int(max/12)+1

        for key in self.keys:
            print("key number",key.getNote().getMidiNumber())

        print(scale)
        self.setScale(scale)

        for key in self.keys:
            print("key number",key.getNote().getMidiNumber())


        for msg in mid.play():
            midioutPort.send(msg) # play sound regardless
            #print(msg)
            if(msg.type in ['note_on','note_off']):
                for key in self.keys:
                    # print("key number",key.getNote().getMidiNumber())
                    # print("midifile num",msg.note) 
                    if msg.note == key.getNote().getMidiNumber():   
                        # print("key number",key.getNote().getMidiNumber())
                        # print("midifile num",msg.note)                     
                        if(msg.type == 'note_on' and msg.velocity > 0):
                            # print("key light")3
                            key.selfPlayActive()
                        
                        elif(msg.type == 'note_off' or msg.velocity == 0):
                            # print("key unlight")
                            key.selfPlayStop()

            if self.exit:
                break   

class Note:
    def __init__(self, name, midiNumber): 
        self.name = name
        self.midiNumber = midiNumber

    def playSound(self):
        msg = mido.Message('note_on', note=self.midiNumber)
        # print(msg)
        #_play_with_simpleaudio(self.sound) 
        midioutPort.send(msg)

    def stopSound(self):
        msg = mido.Message('note_off', note=self.midiNumber)
        #_play_with_simpleaudio(self.sound) 
        midioutPort.send(msg)

    def getSound(self): 
        return self.sound

    def getName(self):
        return self.name

    def getMidiNumber(self):
        return self.midiNumber

class Key: 
    def __init__(self, note, pixel_mappa = None):  # Add back sensor as first input
        # self.sensor = sensor
        self.note = note
        self.state = 0
            #self.releaseSincePlayed = True
            #self.led_on_time = 1.0
            #self.callback_number = 0
            #self.counter = 0
            #self.sensor._queue.start()

        # LEDs linked to key
        self.map = pixel_mappa
        self.LEDState = 0

        warm_white = (253, 244, 220)
        self.dark = Solid(pixel_object=self.map, color = warm_white)
        self.light = Solid(pixel_object=self.map, color =  RED)

        #self.led_timer = threading.Timer(0.1, None)
        
    def __str__(self):
        return self.note.name

    def setUnactiveState(self):
        self.dark.animate()

    def led_on(self):
        # print("turned on LEDs ", self)
        #self.callback_number += 1
        self.LEDState = 1
        self.light.animate()

    def led_off_callback(self, arg):
        # wait for the latest callback before turning off
        if(arg == self.callback_number):
            #print("turned off LEDs ", self)print(msg.note)
            self.dark.animate()

    def led_off(self):
        #print("turned off LEDs ", self)
        self.LEDState = 0
        self.dark.animate()
        
    # Methods
    
    # configuring interrupts
    def makeActive(self):
        self.sensor.when_released = self.notePressed #this is an interupt
        self.sensor.when_pressed = self.noteReleased

    # disabling interrupts
    def makeUnactive(self):
        self.sensor.when_released = None
        self.sensor.when_pressed = None
    
    def notePressed(self): 
        # print("PLAY: ", self.note.getName())
        self.note.playSound()
        # update LEDs here 
        self.led_on()
        self.state = 1

    def noteReleased(self): 
        # print("RELEASE: ", self.note.getName())
        self.note.stopSound()
        
        # update LEDs here - Leave LEDs on for as long as key pressed
        self.led_off()
        self.state = 0
            
    def selfPlayActive(self):
        # update LEDs here 
        #self.led_on()
        # print("self play")
        self.state = 1
        #print(self.note.getName())
    
    def selfPlayStop(self):
        #self.led_off()
        # print("self stop")
        self.state = 0
        
    # Getter and Setters
    def setSensor(self, sensor):
        self.sensor = sensor
         
    def getSensor(self):
        return self.sensor
        
    def setNote(self, note): 
        self.note = note
        
    def getNote(self): 
        return self.note
    
    def getState(self): 
        return self.state

    def getLEDState(self): 
        return self.LEDState
    
    def setState(self, state):
        self.state = state

    def setActiveColour(self, input): 
        self.light = Solid(pixel_object=self.map, color =  input)

    def setUnactiveColour(self, input): 
        self.dark = Solid(pixel_object=self.map, color = input)

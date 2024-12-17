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

warm_white = (253, 244, 220)
midioutPort = mido.open_output('xyz:xyz 129:0')

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
    def SN_read(comport):
        query = f"ADDR:777:SCPI:*SN? \n".encode()
        comport.write(query)
        time.sleep(0.05)
        return comport.read(comport.in_waiting).decode().strip()

    @staticmethod
    def calibrate(comport):
        return ADCInterface.send_command(comport, "TEMP", 0.2)

    @staticmethod
    def reset_adc(comport):
        return ADCInterface.send_command(comport, "LEVEL",0.2)

    @staticmethod
    def read_register(comport):
        return ADCInterface.send_command(comport, "VOLT?",0.2)

    @staticmethod
    def read_adc(comport):
        return ADCInterface.send_command(comport, "CURR", 0.04)

    @staticmethod
    def adc_full_init(comport):
        initialised = False

        for attempt in range(10):
            registers = ADCInterface.read_register(comport)
            if ('38 de' in registers) and ('80 0' in registers) and ('10 40' in registers) and ('28 0' in registers):
                initialised = True
                print('ADC Already Initialised')
                break
            else:
                print(f'ADC Reg returned: {registers} on attempt {attempt}')
                time.sleep(0.5)

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

class Piano: 
    def __init__(self, pixels): 
        self.noOfKeys = 0
        self.noOfNotes = 0
        self.soundType = "piano"
        # key list
        self.keys = []
        self.notes = []
        self.combined = [0] * 24

        self.left_player = 0
        self.right_player = 0

        self.left_LEDs = helper.PixelMap(pixels, PianoPixelMap.left_half_pixel_map, individual_pixels=True)
        self.right_LEDs = helper.PixelMap(pixels, PianoPixelMap.right_half_pixel_map, individual_pixels=True)

        self.exit = False

        self.notSharps = []

        """
        port = mido.open_input('abc', virtual=True)
        print(mido.get_output_names())
        """

        midioutPort = mido.open_output('xyz:xyz 129:0')
        
        # Serial setup
        available_ports = SerialPortManager.find_ports()
        print("Available Ports:", available_ports)

        comport_lists = ["/dev/ttyACM0","/dev/ttyACM1"]

        self.leftSTMComm = 0
        self.rightSTMComm = 0

        while self.leftSTMComm == 0 or self.rightSTMComm == 0:
            for serial_num in comport_lists: 
                initialised_port = SerialPortManager.initialize_port(serial_num)
                print(ADCInterface.SN_read(initialised_port)) 
                if "LEFT" in ADCInterface.SN_read(initialised_port) and self.leftSTMComm == 0: 
                    self.leftSTMComm = initialised_port
                elif "RIGHT" in ADCInterface.SN_read(initialised_port):
                    self.rightSTMComm = initialised_port
  
        # self.leftSTMComm = SerialPortManager.initialize_port(comport_lists[0])
        # self.rightSTMComm = SerialPortManager.initialize_port(comport_lists[1])
        ADCInterface.adc_full_init(self.leftSTMComm)
        ADCInterface.adc_full_init(self.rightSTMComm)

        # FOR DEBUG
        # while True:
        #     print(ADCInterface.read_adc(self.leftSTMComm))
        #     time.sleep(0.001)


        
    def addKey(self, key):
        self.keys.append(key)
        self.noOfKeys += 1

    def addNotSharps(self, key):
        self.notSharps.append(key)

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
                    else: 
                        key.led_off()
            time.sleep(0.05)

    def loop_LEDs_Game(self):
        
        #used for self play - parse midi song
        print("thread started")
        
        while not self.exit:
            for key in self.keys:
                if key.getLEDState() != key.getState():
                    if key.getState() == 1:
                        key.led_on()
                    else: 
                        key.led_off()
            time.sleep(0.1)

    def loop_ADCs(self):
        #used for self play - parse midi song
        print("ADC thread started")
        
        self.left_keys = self.keys[:12]
        self.right_keys = self.keys[12:]

        while not self.exit:
            # Read ADC data for key presses
            left_return = ADCInterface.read_adc(self.leftSTMComm)
            right_return = ADCInterface.read_adc(self.rightSTMComm)

            if (len(left_return) >= 11) and (len(right_return) >= 11): # valid readbacks from both ADCs
                left_return = left_return.split(",")
                right_return = right_return.split(",")

                for index, active_state in enumerate(left_return): 
                    if int(active_state) == 1 and self.left_keys[index].getState() == 1:
                        # Left player pressed an active key
                        self.left_player += 1
                
                for index, active_state in enumerate(right_return): 
                    if int(active_state) == 1 and self.right_keys[index].getState() == 1:
                        # Left player pressed an active key
                        self.right_player += 1

            time.sleep(0.03) #run every 30 ms 

    def exit_loop(self):
        input('Press to exit')
        self.exit = True

    def exit_loop_freeplay(self):
        while not self.exit:
            val = input('Press to exit or change scale')
            try:
                if (int(val) >= 1) and (int(val) <= 6): 
                    self.setScale(int(val))
            except:
                print('Exiting Loop')
                self.exit = True

    def loopKeys(self, active):
        self.resetLights()
        print("Looping all keys")
        # for key in self.keys: 
        #     key.makeActive()
        self.exit = False
        threading.Thread(target=self.exit_loop_freeplay, daemon=True).start()

        while not self.exit:
            for attempt in range(4):
                leftReturn = ADCInterface.read_adc(self.leftSTMComm)
                if  10 < len(leftReturn):
                    break

            for attempt in range(4):
                rightReturn = ADCInterface.read_adc(self.rightSTMComm)
                if  10 < len(rightReturn):
                    break

            # print(leftReturn + ',' + rightReturn) # For debugging
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
                            # threading.Thread(target=key.notePressed(), daemon=True).start()
                        else: 
                            key.noteReleased()
                            # threading.Thread(target=key.notePressed(), daemon=True).start()
                # time.sleep(0.05)

    # def read_in_groups_of_two(self, file_path):
    #     with open(file_path, 'r') as file:
    #         while True:
    #             # Read two lines from the file
    #             line1 = file.readline()
    #             line2 = file.readline()
                
    #             # If both lines are empty, we're at the end of the file
    #             if not line1 and not line2:
    #                 break
                
    #             # Yield the two lines as a tuple (or handle them)
    #             yield (line1.strip(), line2.strip())

    # def or_operation(self, array1, array2):
    #     # Perform element-wise AND operation
    #     return [a | b for a, b in zip(array1, array2)]
    
    def chopsticks(self): 
        self.resetLights()
        print("Playing chopsticks game...")#
         
        # Load the MIDI file for Chopsticks
        midi_song = "TimedGame/Chopsticks_Good.mid"  # Replace with the correct path to your MIDI file
        mid = mido.MidiFile(midi_song)

        for key in self.keys:
            print("key note ", key.getNote().getMidiNumber())

        # Find the appropriate scale for the song
        max_note = max(msg.note for msg in mid if msg.type in ['note_on', 'note_off'])
        scale = int(max_note -1/ 12) - 1
        print("SCALE", scale)
        self.setScale(scale)

        for key in self.keys:
            print("key note ", key.getNote().getMidiNumber())

        # Initialize player scores
        self.left_player = 0
        self.right_player = 0

        # Start LED thread for visual effects
        self.exit = False
        threading.Thread(target=self.loop_LEDs_Game, daemon=True).start()

        # Start ADC thread for tracking the pressed keys vs the active song keys
        threading.Thread(target=self.loop_ADCs, daemon=True).start()

        threading.Thread(target=self.exit_loop, daemon=True).start()

        # Play the MIDI file
        print("Game starting. Follow the lights!")

        # just play the song
        for msg in mid.play():
            # Send the MIDI message to play the sound
            midioutPort.send(msg)
            print(msg)

            # Handle note events
            if msg.type in ['note_on', 'note_off']:
                print("here2")
                for key in self.keys:
                    # print("key note ", key.getNote().getMidiNumber())
                    # print("midi note ", msg.note)
                         
                    if msg.note == key.getNote().getMidiNumber():
                        print("here")
                        if msg.type == 'note_on' and msg.velocity > 0:
                            key.selfPlayActive()  # Light up the key
                        elif msg.type == 'note_off' or msg.velocity == 0:
                            key.selfPlayStop()  # Turn off the light

            if self.exit:
                break

        # Display the results
        print("Game Over!")
        print(f"Player 1 Score: {self.left_player}")
        print(f"Player 2 Score: {self.right_player}")

        if self.left_player > self.right_player:
            print("Player 1 wins!")
            #light up LEDs green for left
            left_color = GREEN
            right_color = RED
            
        elif self.right_player > self.left_player:
            print("Player 2 wins!")
            #light up LEDs green for right
            left_color = RED
            right_color = GREEN
        else:
            print("It's a tie!")
            #light up LEDs Rainbow
            left_color = GREEN
            right_color = GREEN

        # communicate the results by lighting up the LED for the winner...
        for i in range(10):
            Solid(pixel_object=self.left_LEDs, color = left_color).animate()
            Solid(pixel_object=self.right_LEDs, color = right_color).animate()
            time.sleep(0.33)
            
            Solid(pixel_object=self.left_LEDs, color = warm_white).animate()
            Solid(pixel_object=self.right_LEDs, color = warm_white).animate()
            time.sleep(0.33)
                    
    def countKeys(self):
        return self.noOfKeys
            
    def reset(self):
        self.noOfKeys = 0
        self.soundType = "piano"
        self.keys = []

    def setScale(self, scale_select): 
        
        if (scale_select >= 1) and (scale_select <= 6):
            if scale_select == 1: 
                scale_select = 0
            elif scale_select == 2: 
                scale_select = 12
            elif scale_select == 3: 
                scale_select = 24
            elif scale_select == 4: 
                scale_select = 36
            elif scale_select == 5:
                scale_select = 48
            elif scale_select == 6:  
                scale_select = 60
            for key in self.keys:
                print(scale_select)
                key.setNote(self.notes[scale_select])
                scale_select+=1
        else: 
            print("Invalid Scale Input")

    def parseSongMidi(self, midiSong):
        self.resetLights()

        threading.Thread(target=self.loop_LEDs, daemon=True).start()

        self.exit = False
        threading.Thread(target=self.exit_loop, daemon=True).start()

        mid = mido.MidiFile(midiSong)
        
        # Determine the scale based on the highest note in the MIDI file
        max_note = max(msg.note for msg in mid if msg.type in ['note_on', 'note_off'])
        scale = (max_note // 12) + 1
        print(f"Detected scale: {scale}")

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

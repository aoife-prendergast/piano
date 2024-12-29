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
LED_COUNT = 2245

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
    def send_command(comport, command, delay=0.05, int_data=1):
        query = f"ADDR:777:ADC:MEAS:{command} {int_data} (@0)\n".encode()
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

    def set_threshold(comport, threshold):
        return ADCInterface.send_command(comport, "POW", 0.04, threshold)

    @staticmethod
    def adc_full_init(comport):
        initialised = False

        # Intitialise is fast now, better to re-intisialise everytime
        # for attempt in range(3):
        #     registers = ADCInterface.read_register(comport)
        #     if ('38 de' in registers) and ('80 0' in registers) and ('10 40' in registers) and ('28 0' in registers):
        #         initialised = True
        #         print('ADC Already Initialised')
        #         break
        #     else:
        #         print(f'ADC Reg returned: {registers} on attempt {attempt}')
        #         time.sleep(0.5)

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
        self.pixel = pixels

        self.left_LEDs = helper.PixelMap(self.pixel, PianoPixelMap.left_half_pixel_map, individual_pixels=True)
        self.right_LEDs = helper.PixelMap(self.pixel, PianoPixelMap.right_half_pixel_map, individual_pixels=True)

        self.exit = False

        self.notSharps = []

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
                if "LEFT" in ADCInterface.SN_read(initialised_port) and self.leftSTMComm == 0: 
                    self.leftSTMComm = initialised_port
                elif "RIGHT" in ADCInterface.SN_read(initialised_port):
                    self.rightSTMComm = initialised_port

        ADCInterface.adc_full_init(self.leftSTMComm)
        ADCInterface.adc_full_init(self.rightSTMComm)

        # FOR DEBUG
        # while True:
        #     print(ADCInterface.read_adc(self.leftSTMComm))
        #     time.sleep(0.001)

    def reinitialiseADC(self):
        ADCInterface.reset_adc(self.leftSTMComm)
        time.sleep(0.5)
        ADCInterface.initialize(self.leftSTMComm)
        time.sleep(0.2)
        ADCInterface.reset_adc(self.rightSTMComm)
        time.sleep(0.5)
        ADCInterface.initialize(self.rightSTMComm)
        time.sleep(0.2)
        
    def addKey(self, key):
        self.keys.append(key)
        self.noOfKeys += 1

    def addNotSharps(self, key):
        self.notSharps.append(key)

    def addNotes(self, notes):
        self.notes = self.notes + notes
        self.noOfNotes = len(self.notes)

    def showGameResult(self):
        print("Setting all key unactive colors")
        for key in self.keys:
            key.showGameColor()
        self.updateLEDs()
        
    def resetLights(self):
        print("Setting all key unactive colors")
        for key in self.keys:
            key.setUnactiveState()
        self.updateLEDs()

    def calibrate_ADCs(self): 
        ADCInterface.calibrate(self.leftSTMComm)
        ADCInterface.calibrate(self.rightSTMComm)

    def set_ADC_threshold(self, threshold):
        ADCInterface.set_threshold(self.leftSTMComm, threshold)
        ADCInterface.set_threshold(self.rightSTMComm, threshold)

    def updateLEDs(self): 
        current_index = 0
        for key in self.keys: 
            for i in range(current_index, current_index + key.getLEDBlockSize()): 
                if i < LED_COUNT:  # Ensure we don't exceed the total number of LEDs
                    self.pixel[i] = key.getLEDColor()
            current_index += key.getLEDBlockSize()
        self.pixel.show()

    def loop_LEDs(self):
        
        #used for self play - parse midi song
        print("LED thread started")
        
        while not self.exit:
            self.updateLEDs()


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

            time.sleep(0.01) #run every 30 ms 

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
        threading.Thread(target=self.loop_LEDs, daemon=True).start()

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
        self.exit = True

    
    def chopsticks(self): 
        self.resetLights()
        print("Playing chopsticks game...")
        
        # Initialise the pixelmap for games
        self.game_map = []

        # Load the MIDI file for Chopsticks
        midi_song = "TimedGame/Chopsticks_Good_2.mid"  # Replace with the correct path to your MIDI file
        mid = mido.MidiFile(midi_song)

        # Find the appropriate scale for the song
        max_note = max(msg.note for msg in mid if msg.type in ['note_on', 'note_off'])
        scale = int((max_note - 1)/ 12) -2 # should be -1 for everything but -2 from max for custom chopsticks midi
        print("SCALE", scale)
        self.setScale(scale)

        # Initialize player scores
        self.left_player = 0
        self.right_player = 0

        # Start LED thread for visual effects
        self.exit = False
        threading.Thread(target=self.loop_LEDs, daemon=True).start()

        # Start ADC thread for tracking the pressed keys vs the active song keys
        threading.Thread(target=self.loop_ADCs, daemon=True).start()

        threading.Thread(target=self.exit_loop, daemon=True).start()

        # Play the MIDI file
        print("Game starting. Follow the lights!")

        # just play the song
        for msg in mid.play():
            # Send the MIDI message to play the sound
            midioutPort.send(msg)

            # Handle note events
            if msg.type in ['note_on', 'note_off']:
                for val, key in enumerate(self.keys):
                         
                    if msg.note == key.getNote().getMidiNumber():
                        if msg.type == 'note_on' and msg.velocity > 0:
                            key.gamePlay()  # Turn ON the light
                        elif msg.type == 'note_off' or msg.velocity == 0:
                            key.gameStop()  # Turn OFF the light

            if self.exit:
                break

        self.exit = True

        # Display the results
        print("Game Over!")
        print(f"Player 1 Score: {self.left_player}")
        print(f"Player 2 Score: {self.right_player}")


        if self.left_player > self.right_player:
            print("Player 1 wins!")
            #light up LEDs green for left
            for key in self.left_keys: 
                key.setGameColor(GREEN)
            for key in self.right_keys: 
                key.setGameColor(RED)
            
        elif self.right_player > self.left_player:
            print("Player 2 wins!")
            #light up LEDs green for right
            for key in self.left_keys: 
                key.setGameColor(RED)
            for key in self.right_keys: 
                key.setGameColor(GREEN)

        else:
            print("It's a tie!")
            #light up LEDs Rainbow
            for key in self.keys: 
                key.setGameColor(ORANGE)


        # communicate the results by lighting up the LED for the winner...
        for i in range(4):
            self.showGameResult()
            time.sleep(0.5)
            
            self.resetLights()
            time.sleep(0.25)
        
        for key in self.keys: 
            key.setGameColor(BLUE)
                    
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
                print(f'Note before: {key.getNote().getMidiNumber()}')
                print(scale_select)
                key.setNote(self.notes[scale_select])
                print(f'Note after: {key.getNote().getMidiNumber()}')
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

        self.exit = True

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
    def __init__(self, note, LEDLen, pixel_mappa = None):  # Add back sensor as first input
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
        self.LEDCurrentColor = warm_white

        self.dark = Solid(pixel_object=self.map, color = warm_white)
        self.light = Solid(pixel_object=self.map, color =  RED)

        self.LEDActiveColor = warm_white
        self.LEDUnactiveColor = warm_white
        #self.led_timer = threading.Timer(0.1, None)

        self.gameColor = BLUE

        self.LEDBlockSize = LEDLen
        
    def __str__(self):
        return self.note.name

    def setUnactiveState(self):
        self.LEDCurrentColor = self.LEDUnactiveColor

    def showGameColor(self):
        self.LEDCurrentColor = self.gameColor

    def setGameColor(self, input):
        self.gameColor = input

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
        #self.led_on()
        self.LEDCurrentColor = self.LEDActiveColor
        self.state = 1

    def noteReleased(self): 
        # print("RELEASE: ", self.note.getName())
        self.note.stopSound()
        
        # update LEDs here - Leave LEDs on for as long as key pressed
        #self.led_off()
        self.LEDCurrentColor = self.LEDUnactiveColor
        self.state = 0
            
    def selfPlayActive(self):
        # update LEDs here 
        #self.led_on()
        # print("self play")
        self.state = 1
        self.LEDCurrentColor = self.LEDActiveColor
        #print(self.note.getName())
    
    def selfPlayStop(self):
        #self.led_off()
        # print("self stop")
        self.state = 0
        self.LEDCurrentColor = self.LEDUnactiveColor

    def gamePlay(self):
        self.LEDCurrentColor = self.LEDActiveColor
        self.state = 1
    
    def gameStop(self):
        self.LEDCurrentColor = self.LEDUnactiveColor
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

    def getLEDColor(self): 
        return self.LEDCurrentColor

    def getLEDState(self): 
        return self.LEDState
    
    def setState(self, state):
        self.state = state

    def setActiveColour(self, input): 
        self.LEDActiveColor = input
        self.light = Solid(pixel_object=self.map, color =  input)

    def setUnactiveColour(self, input): 
        self.LEDUnactiveColor = input
        self.dark = Solid(pixel_object=self.map, color = input)

    def getLEDBlockSize(self):
        return self.LEDBlockSize

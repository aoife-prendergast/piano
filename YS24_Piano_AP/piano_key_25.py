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

        for attempt in range(3):
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
        self.pixel = pixels
        self.exit = False
        #score for game...
        self.left_player = 0
        self.right_player = 0

        midioutPort = mido.open_output('xyz:xyz 129:0')
        
        # Serial setup
        available_ports = SerialPortManager.find_ports()
        print("Available Ports:", available_ports)

        comport_lists = ["/dev/ttyACM0","/dev/ttyACM1"]
        self.leftSTMComm = None
        self.rightSTMComm = ModuleNotFoundError

        while self.leftSTMComm == None or self.rightSTMComm == None:
            for serial_num in comport_lists: 
                initialised_port = SerialPortManager.initialize_port(serial_num)
                if "LEFT" in ADCInterface.SN_read(initialised_port) and self.leftSTMComm == 0: 
                    self.leftSTMComm = initialised_port
                elif "RIGHT" in ADCInterface.SN_read(initialised_port):
                    self.rightSTMComm = initialised_port

        ADCInterface.adc_full_init(self.leftSTMComm)
        ADCInterface.adc_full_init(self.rightSTMComm)

    def updateLEDs(self): 
        current_index = 0
        for key in self.keys: 
            for i in range(current_index, current_index + key.getLEDBlockSize()): 
                if i < LED_COUNT:  # Ensure we don't exceed the total number of LEDs
                    self.pixel[i] = key.getLEDColor()
            current_index += key.getLEDBlockSize()
        self.pixel.show()
        
    def addKey(self, key):
        self.keys.append(key)
        self.noOfKeys += 1

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


    def loop_LEDs(self):
        print("LED thread started")
        while not self.exit:
            self.updateLEDs()

    def loop_ADCs(self):
        #used for self play - parse midi song
        print("ADC thread started")

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

            time.sleep(0.01) #run every 10 ms 

    def exit_loop(self):
        input("\n!Press to exit!!!")
        self.exit = True

    def exit_loop_freeplay(self):
        while not self.exit:
            val = input('\nPress to exit or 1-6 to change scale')
            try:
                if (int(val) >= 1) and (int(val) <= 6): 
                    self.setScale(int(val))
            except:
                print('Exiting Loop')
                self.exit = True

    def loopKeys(self, active):
        self.resetLights()
        print("Looping all keys")

        self.exit = False
        threading.Thread(target=self.exit_loop_freeplay, daemon=True).start()
        threading.Thread(target=self.loop_LEDs, daemon=True).start()

        while not self.exit:
            leftReturn, rightReturn = "", ""
            for _ in range(4):  # Attempt up to 4 times
                if len(leftReturn) < 10:
                    leftReturn = ADCInterface.read_adc(self.leftSTMComm)
                if len(rightReturn) < 10:
                    rightReturn = ADCInterface.read_adc(self.rightSTMComm)
                if len(leftReturn) >= 10 and len(rightReturn) >= 10:
                    break

            # print(leftReturn + ',' + rightReturn) # For debugging
            # Validate data length before processing
            if (len(leftReturn) >= 23) and (len(rightReturn) >= 23): 
                combined = (leftReturn + "," + rightReturn).split(",")
                #print(combined)

                for val, key in enumerate(self.keys):
                    if key.getState() != int(combined[val]):
                        if int(self.combined[val]) == 1:
                            key.notePressed()
                        else: 
                            key.noteReleased()
                # time.sleep(0.05)
        self.exit = True

    
    def chopsticks(self): 
        self.left_keys = self.keys[:12]
        self.right_keys = self.keys[12:]

        self.resetLights()
        print("Playing chopsticks game...")

        # Load the MIDI file for Chopsticks
        midi_song = "TimedGame/Chopsticks_Good_2.mid"  # Replace with the correct path to your MIDI file
        mid = mido.MidiFile(midi_song)

        # Find the appropriate scale for the song
        max_note = max(msg.note for msg in mid if msg.type in ['note_on', 'note_off'])
        scale = int((max_note - 1)/ 12) -2 # should be -1 for everything but -2 from max for custom chopsticks midi
        print("SCALE :", scale)
        self.setScale(scale)

        # Initialize player scores
        self.left_player = 0
        self.right_player = 0

        # Start LED thread for visual effects
        self.exit = False
        threading.Thread(target=self.loop_LEDs, daemon=True).start()
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
        self.exit = False

        threading.Thread(target=self.loop_LEDs, daemon=True).start()
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
                    if msg.note == key.getNote().getMidiNumber():                     
                        if(msg.type == 'note_on' and msg.velocity > 0):
                            key.selfPlayActive()
                        elif(msg.type == 'note_off' or msg.velocity == 0):
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
        midioutPort.send(msg)

    def stopSound(self):
        msg = mido.Message('note_off', note=self.midiNumber)
        midioutPort.send(msg)

    def getSound(self): 
        return self.sound

    def getName(self):
        return self.name

    def getMidiNumber(self):
        return self.midiNumber

class Key: 
    def __init__(self, note, LEDLen, pixel_mappa = None):  # Add back sensor as first input
        self.note = note
        self.state = 0

        # LEDs linked to key
        self.map = pixel_mappa
        self.LEDCurrentColor = warm_white

        self.LEDActiveColor = warm_white
        self.LEDUnactiveColor = warm_white
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
    
    def notePressed(self): 
        # print("PLAY: ", self.note.getName())
        self.note.playSound()
        self.LEDCurrentColor = self.LEDActiveColor
        self.state = 1

    def noteReleased(self): 
        # print("RELEASE: ", self.note.getName())
        self.note.stopSound()
        self.LEDCurrentColor = self.LEDUnactiveColor
        self.state = 0
            
    def selfPlayActive(self):
        self.state = 1
        self.LEDCurrentColor = self.LEDActiveColor
    
    def selfPlayStop(self):
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

    def setUnactiveColour(self, input): 
        self.LEDUnactiveColor = input

    def getLEDBlockSize(self):
        return self.LEDBlockSize

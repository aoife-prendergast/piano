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
import pygame
import time
import threading
from threading import Thread 
from time import sleep
import mido

from adc import ADC

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
midioutPort = mido.open_output('xyz:xyz 129:0')

class Piano: 
    def __init__(self): 
        self.noOfKeys = 0
        self.noOfNotes = 0
        self.soundType = "piano"
        # key list
        self.keys = []
        self.notes = []

        port = mido.open_input('abc', virtual=True)
        print(mido.get_output_names())
        midioutPort = mido.open_output('xyz:xyz 129:0')
        
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

<<<<<<< HEAD
        self.leftSTMComm = serial.Serial("/dev/ttyACM0",baudrate=115200,)
=======
        #self.leftSTMComm = serial.Serial("/dev/ttyACM0",baudrate=115200,)
>>>>>>> ebbd4e74fdcc9eb208b6e0fe8663a8073344bd70
        #self.rightSTMComm = serial.Serial('COM5',baudrate=115200,)

        """
        pixel_pin = pixel_pin_x
        pixel_num = pixel_pin_x
        pixels = pixels_x
        """

        self.left_adc = ADC()
        self.left_adc.adc_setup()

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

    def loopKeys(self, active):
        print("Looping all keys")
        while True:
<<<<<<< HEAD
            query = str(f"ADDR:777:ADC:MEAS:VOLT 1.0 (@6)\n")

            #read left STM values
            self.leftSTMComm.write(query.encode())
            time.sleep(0.1)
            leftReturn = self.leftSTMComm.read()

            #read right STM values
            #self.rightSTMComm.write("ADDR:777:ADC:MEAS:VOLT 1.0 (@6)\n")
            #rightReturn = self.rightSTMComm.read()

            #only continue if both ports turned status
            if leftReturn: 
                print(leftReturn)
                combined = leftReturn.split(", ")
                #combined = leftReturn.split(", ") + rightReturn.split(", ")
                for key,val in enumerate(self.keys):
                    if key.getState() != combined[val]:
                        #there has been a state change
                        if key.getState() == 1:
                            key.NotePressed()
                        else: 
                            key.noteReleased()
        
            time.sleep(0.5)
=======
            combined = self.left_adc.adc_read()
            #print(combined)
            count = 0
            for key in self.keys:
                if key.getState() != combined[count]:
                    #there has been a state change
                    if combined[count]== 1:
                        key.notePressed()
                    else: 
                        key.noteReleased()
                count+=1
            time.sleep(0.0050)
>>>>>>> ebbd4e74fdcc9eb208b6e0fe8663a8073344bd70
                    
    def countKeys(self):
        return self.noOfKeys
            
    def reset(self):
        self.noOfKeys = 0
        self.soundType = "piano"
        self.keys = []

    def setScale(self, scale_select): 
        
        if (scale_select >= 2) and (scale_select <= 5):
            scale_select -= 2
            scale_select = scale_select*12
            for key in self.keys:
                print(scale_select)
                key.setNote(self.notes[scale_select])
                scale_select+=1
        else: 
            print("Invalid Scale Input")

    def parseSongMidi(self, midiSong): 

        delay = 3
        # Strips the newline character
        mid = mido.MidiFile(midiSong)
        for msg in mid.play():
            found = False
            if(msg.channel == 0 or msg.channel == 1):
                midioutPort.send(msg)
                #print(msg)
                for key in self.keys:
                    if(msg.type == 'note_on' or msg.type == 'note_off'):
                        if msg.note == key.getNote().getMidiNumber():
                            #print("note found")
                            
                            if(msg.type == 'note_on'):
                                #print("key.lightKey()")
                                key.selfPlayActive()
                            """
                            if(msg.type == 'note_off'):
                                print("key.unlightKey()")
                                key.selfPlayStop()
                            """
                            break                

class Note:
    def __init__(self, name, midiNumber): 
        self.name = name
        self.state = False
        self.midiNumber = midiNumber

    def playSound(self):
        msg = mido.Message('note_on', note=self.midiNumber)
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
    def __init__(self, note, pixel_mappa = None): 
        self.note = note
        self.state = 0
        self.releaseSincePlayed = True
        self.led_on_time = 1.0
        self.callback_number = 0
        #self.sensor._queue.start()
        #todo
        # LEDs linked to key
        self.map = pixel_mappa

        warm_white = (253, 244, 220)
        self.dark = Solid(pixel_object=self.map, color = warm_white)
        self.light = Solid(pixel_object=self.map, color =  RED)

        self.dark.animate()

        self.led_timer = threading.Timer(0.1, None)
        
    def __str__(self):
        return self.note.name

    def setUnactiveState(self):
        self.dark.animate()

    def led_on(self):
        # print("turned on LEDs ", self)
        self.callback_number += 1
        self.light.animate()

    def led_off_callback(self, arg):
        # wait for the latest callback before turning off
        if(arg == self.callback_number):
            #print("turned off LEDs ", self)
            self.dark.animate()

    def led_off(self):
        #print("turned off LEDs ", self)
        self.dark.animate()
        
    # Methods
    """
    # configuring interrupts
    def makeActive(self):
        self.sensor.when_released = self.notePressed #this is an interupt
        self.sensor.when_pressed = self.noteReleased

    # disabling interrupts
    def makeUnactive(self):
        self.sensor.when_released = None
        self.sensor.when_pressed = None
    """
    def notePressed(self): 
        print("PLAY: ", self.note.getName())
        self.note.playSound()
        # update LEDs here 
        self.led_on()
        #self.led_timer = threading.Timer(self.led_on_time, self.led_off_callback, (self.callback_number,))
        #self.led_timer.start()
        self.state = 1

    def noteReleased(self): 
        print("RELEASE: ", self.note.getName())
        self.note.stopSound()
        
        # update LEDs here - Leave LEDs on for as long as key pressed
        self.led_off()
        #self.led_timer.cancel()
        self.state = 0
            
    def selfPlayActive(self):
        # update LEDs here 
        self.led_on()
        self.led_timer = threading.Timer(self.led_on_time, self.led_off_callback, (self.callback_number,))
        self.led_timer.start()
    
    def selfPlayStop(self):
        self.led_off()
        self.callback_number += 1
        #self.led_timer.cancel()
        
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
    
    def setState(self, state):
        self.state = state

    def setActiveColour(self, input): 
        self.light = Solid(pixel_object=self.map, color =  input)

    def setUnactiveColour(self, input): 
        self.dark = Solid(pixel_object=self.map, color = input)

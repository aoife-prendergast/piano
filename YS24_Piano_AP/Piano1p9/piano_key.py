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
import digitalio
from pixel_mapping import PianoPixelMap
"""
global pixel_pin
global pixel_num 
global pixels
"""

class Piano: 
    def __init__(self): 
        self.noOfKeys = 0
        self.noOfNotes = 0
        self.soundType = "piano"
        # key list
        self.keys = []
        self.notes = []

        port = mido.open_input('xyz', virtual=True)
        print(mido.get_output_names())
        self.midiout = mido.open_output('xyz:xyz 129:0')

        """
        pixel_pin = pixel_pin_x
        pixel_num = pixel_pin_x
        pixels = pixels_x
        """

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
        for key in self.keys:
            if active:
                key.makeActive()
            else: 
                key.makeUnactive()
        """
        time_old = time.perf_counter()
        time_taken = time.perf_counter()
        for key in self.keys:
            key.playSound()

            time_taken = time.perf_counter() - time_old
            print("Key: ", key.getName(), key.checkForce(), " -> time: ", time_taken)
            time_old = time_taken
        """
                
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
                self.midiout.send(msg)
                #print(msg)
                for key in self.keys:
                    if msg.note == key.getNote().getMidiNumber():
                        #print("note found")
                        if(msg.type == 'note_on'):
                            print("key.lightKey()")
                        if(msg.type == 'note_off'):
                            print("key.unlightKey()")


class Note:
    def __init__(self, name, sound, midiNumber): 
        self.name = name
        self.sound = sound
        self.state = False
        self.midiNumber = midiNumber

    def playSound(self):
        _play_with_simpleaudio(self.sound) 
        #self.sound.play()

    def getSound(self): 
        return self.sound

    def getName(self):
        return self.name

    def getMidiNumber(self):
        return self.midiNumber

class Key: 
    def __init__(self, sensor, note, pixel_mappa = None): 
        self.sensor = sensor 
        self.note = note
        self.state = False
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
        
    def __str__(self):
        return self.note.name

    def setUnactiveState(self):
        self.dark.animate()

    def led_on(self):
        # print("turned on LEDs ", self)
        self.callback_number += 1
        self.light.animate()

    def led_off_callback(self, arg):
        if(arg == self.callback_number):
            #print("turned off LEDs ", self)
            self.dark.animate()
        
    # Methods
    def makeActive(self):
        self.sensor.when_released = self.noteActive
    
    def makeUnactive(self):
        self.sensor.when_released = None

    def noteActive(self): 
        #print("PLAY: ", self.note.getName())
        self.note.playSound()
        
        # update LEDs here 
        self.led_on()
        led_timer = threading.Timer(self.led_on_time, self.led_off_callback, (self.callback_number,))
        led_timer.start()
            
    def playSoundSong(self):
        # print(self.note.getSound().get_length())
        #self.note.playSound()
        self.noteActive()
    
    def stopSoundSong(self):
        self.note.stop()
        
    # Getter and Setters
    def setSensor(self, sensor):
        self.sensor = sensor
      
    def getName(self): 
        return self.name
         
    def getSensor(self): 
        return self.sensor
        
    def setNote(self, note): 
        self.note = note
        
    def getNote(self): 
        return self.note
    
    def getState(self): 
        return self.state

    def setActiveColour(self, input): 
        self.light = Solid(pixel_object=self.map, color =  input)

    def setUnactiveColour(self, input): 
        self.dark = Solid(pixel_object=self.map, color = input)

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

from adafruit_led_animation import helper
from adafruit_led_animation.color import BLACK
from adafruit_led_animation.color import RED
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
        
    def parseSong(self, song): 
        self.song = song
        path = 'Songs/' + song
        f = open(path, 'r')
        lines = f.readlines()
        #print(pygame.mixer.get_num_channels())
        #chan = pygame.mixer.find_channel()
        
        count = 0
        allowPlay = False
        nextLineParseSpeed = False
        # Strips the newline character
        for line in lines:
            values = []
            parsedNotes = []
            found = False
            
            count += 1
            content = line.strip()
            #print("Line{}: {}".format(count, content))
            if allowPlay:
                print("z")
                parsedNotes = content.split(" ")
                for noteRead in parsedNotes: 
                    found = False
                    print(noteRead)
                    if (noteRead == "|"): 
                        pass
                    elif (noteRead == "...") or (noteRead == "---"): 
                        time.sleep(0.15)
                    else: 
                        for key in self.keys:
                            if noteRead == key.getNote().getName():
                                print("note found")
                                found = True
                                key.playSoundSong()
                        # we still want to play the note even if it istn't currently active for a key
                        if not found: 
                            for note in self.notes:
                                if noteRead == note.getName():
                                    print("note found")
                                    found = True
                                    note.playSound()
                        if not found:
                            print(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NOTE NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" )
                        time.sleep(0.15) # speed
            elif nextLineParseSpeed: 
                values = content.split(":")
                #speed = int(values[0])/int(values[1])
                nextLineParseSpeed = False
            elif content.find("SPEED") != -1:
                nextLineParseSpeed = True
                print("x")
            elif content.find("VOICE0") != -1:
                break
            elif content.find("VOICE") != -1:
                allowPlay = True 
                print("y")
            

                    #key.stopSoundSong()

class Note:
    def __init__(self, name, sound): 
        self.name = name
        self.sound = sound
        self.state = False

    def playSound(self): 
        self.sound.play()

    def getSound(self): 
        return self.sound

    def getName(self): 
        return self.name

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

        self.dark = Solid(pixel_object=self.map, color = BLACK)
        self.light = Solid(pixel_object=self.map, color = RED)
        
    def __str__(self):
        return self.note.name

    def led_on(self):
        print("turned on LEDs ", self)
        self.callback_number += 1
        self.light.animate()

    def led_off_callback(self, arg):
        if(arg == self.callback_number):
            print("turned off LEDs ", self)
            self.dark.animate()
        
    # Methods
    def makeActive(self):
        self.sensor.when_released = self.noteActive
    
    def makeUnactive(self):
        self.sensor.when_released = None

    def noteActive(self): 
        print("PLAY: ", self.note.getName())
        self.note.playSound()
        
        # update LEDs here 
        self.led_on()
        led_timer = threading.Timer(self.led_on_time, self.led_off_callback, (self.callback_number,))
        led_timer.start()
            
    def playSoundSong(self):
        print(self.note.getSound().get_length())
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

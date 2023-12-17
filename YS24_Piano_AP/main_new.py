#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
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
"""
from piano_key import Key 
from piano_key import Piano
from piano_key import Note
"""
import pygame
from pygame import mixer
import time
import random
from gpiozero import *
import pygame._sdl2.audio as sdl2_audio
from pydub import AudioSegment
import simpleaudio
from pydub.playback import _play_with_simpleaudio

#from adafruit_led_animation import helper
#from adafruit_led_animation.color import *
#import board
#import neopixel
"""
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.sequence import AnimationSequence
"""
#import digitalio
#from pixel_mapping import PianoPixelMap

AUDIO_OUTPUT = False

def main(args):

    pygame.init()

    print(pygame.mixer.get_init())
    while(1):   
        #the sounds 
        #Cn2 = pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Cn2.wav")


        Cn2 = AudioSegment.from_wav("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Cn2.wav")
        Cs2 = AudioSegment.from_wav("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/C#2.wav")
        Dn2 = AudioSegment.from_wav("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Dn2.wav")

        _play_with_simpleaudio(Cn2)
        _play_with_simpleaudio(Cs2)
        _play_with_simpleaudio(Dn2)

        time.sleep(5)
        
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

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
    pygame.mixer.pre_init(44100,-16,2)
    pygame.init()
    pygame.mixer.init(44100,-16,2)
    print(pygame.mixer.get_init())

    pygame.mixer.quit()

    print(pygame.mixer.get_init())
 
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

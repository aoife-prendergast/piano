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

from piano_key import Key 
from piano_key import Piano
from piano_key import Note
import pygame
from pygame import mixer
import time
import random
from gpiozero import *
import RPi.GPIO as GPIO

from adafruit_led_animation import helper
from adafruit_led_animation.color import *
import board
import neopixel

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.sequence import AnimationSequence

import digitalio
from pixel_mapping import PianoPixelMap

def main(args):

    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    pygame.init()
    #pygame.mixer.init(44100, -16,2,2048)

    print(pygame.mixer.get_init())
    
    #the sounds 
    Cn2 = Note("Cn2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Cn2.wav"))
    Cs2 = Note("C#2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/C#2.wav"))
    Dn2 = Note("Dn2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Dn2.wav"))
    Ds2 = Note("D#2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/D#2.wav"))
    En2 = Note("En2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/En2.wav"))
    Fn2 = Note("Fn2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Fn2.wav"))
    Fs2 = Note("F#2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/F#2.wav"))
    Gn2 = Note("Gn2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Gn2.wav"))
    Gs2 = Note("G#2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/G#2.wav"))
    An2 = Note("An2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/An2.wav"))
    As2 = Note("A#2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/A#2.wav"))
    Bn2 = Note("Bn2",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Bn2.wav"))
    Cn3 = Note("Cn3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Cn3.wav"))
    Cs3 = Note("C#3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/C#3.wav"))
    Dn3 = Note("Dn3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Dn3.wav"))
    Ds3 = Note("D#3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/D#3.wav"))
    En3 = Note("En3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/En3.wav"))
    Fn3 = Note("Fn3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Fn3.wav"))
    Fs3 = Note("F#3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/F#3.wav"))
    Gn3 = Note("Gn3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Gn3.wav"))
    Gs3 = Note("G#3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/G#3.wav"))
    An3 = Note("An3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/An3.wav"))
    As3 = Note("A#3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/A#3.wav"))
    Bn3 = Note("Bn3",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Bn3.wav"))
    Cn4 = Note("Cn4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Cn4.wav"))
    Cs4 = Note("C#4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/C#4.wav"))
    Dn4 = Note("Dn4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Dn4.wav"))
    Ds4 = Note("D#4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/D#4.wav"))
    En4 = Note("En4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/En4.wav"))
    Fn4 = Note("Fn4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Fn4.wav"))
    Fs4 = Note("F#4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/F#4.wav"))
    Gn4 = Note("Gn4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Gn4.wav"))
    Gs4 = Note("G#4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/G#4.wav"))
    An4 = Note("An4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/An4.wav"))
    As4 = Note("A#4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/A#4.wav"))
    Bn4 = Note("Bn4",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Bn4.wav"))
    Cn5 = Note("Cn5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Cn5.wav"))
    Cs5 = Note("C#5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/C#5.wav"))
    Dn5 = Note("Dn5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Dn5.wav"))
    Ds5 = Note("D#5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/D#5.wav"))
    En5 = Note("En5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/En5.wav"))
    Fn5 = Note("Fn5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Fn5.wav"))
    Fs5 = Note("F#5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/F#5.wav"))
    Gn5 = Note("Gn5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Gn5.wav"))
    Gs5 = Note("G#5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/G#5.wav"))
    An5 = Note("An5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/An5.wav"))
    As5 = Note("A#5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/A#5.wav"))
    Bn5 = Note("Bn5",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Bn5.wav"))
    Cn6 = Note("Cn6",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Cn6.wav"))
    Cs6 = Note("C#6",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/C#6.wav"))
    Dn6 = Note("Dn6",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/Dn6.wav"))
    Ds6 = Note("D#6",pygame.mixer.Sound("/home/relhwpi/Projects/piano/YS24_Piano_AP/Sounds/D#6.wav"))
    
    #key1 = Key("do", SmoothedInputDevice(21), sound1)
    
    """
    key_Cn3 = Key("Cn3", Button(21), Cn3)
    key_Cs3 = Key("C#3", Button(20), Cs3)
    key_Dn3 = Key("Dn3", Button(26), Dn3)
    key_Ds3 = Key("D#3", Button(0), Ds3)
    key_En3 = Key("En3", Button(1), En3)
    key_Fn3 = Key("Fn3", Button(2), Fn3)
    key_Fs3 = Key("F#3", Button(3), Fs3)
    key_Gn3 = Key("Gn3", Button(4), Gn3)
    key_Gs3 = Key("G#3", Button(5), Gs3)
    key_An3 = Key("An3", Button(6), An3)
    key_As3 = Key("A#3", Button(23), As3)
    key_Bn3 = Key("Bn3", Button(24), Bn3)
    """

    pixel_pin = board.D18
    pixel_num = 2500
    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.3, auto_write=False)

    key1map = helper.PixelMap(pixels, PianoPixelMap.key_1_pixel_map, individual_pixels=True)
    key2map = helper.PixelMap(pixels, PianoPixelMap.key_2_pixel_map, individual_pixels=True)
    key3map = helper.PixelMap(pixels, PianoPixelMap.key_3_pixel_map, individual_pixels=True)
    key4map = helper.PixelMap(pixels, PianoPixelMap.key_4_pixel_map, individual_pixels=True)
    key5map = helper.PixelMap(pixels, PianoPixelMap.key_5_pixel_map, individual_pixels=True)
    key6map = helper.PixelMap(pixels, PianoPixelMap.key_6_pixel_map, individual_pixels=True)
    key7map = helper.PixelMap(pixels, PianoPixelMap.key_7_pixel_map, individual_pixels=True)
    key8map = helper.PixelMap(pixels, PianoPixelMap.key_8_pixel_map, individual_pixels=True)
    key9map = helper.PixelMap(pixels, PianoPixelMap.key_9_pixel_map, individual_pixels=True)
    key10map = helper.PixelMap(pixels, PianoPixelMap.key_10_pixel_map, individual_pixels=True)
    key11map = helper.PixelMap(pixels, PianoPixelMap.key_11_pixel_map, individual_pixels=True)
    key12map = helper.PixelMap(pixels, PianoPixelMap.key_12_pixel_map, individual_pixels=True)
    key13map = helper.PixelMap(pixels, PianoPixelMap.key_13_pixel_map, individual_pixels=True)
    key14map = helper.PixelMap(pixels, PianoPixelMap.key_14_pixel_map, individual_pixels=True)
    key15map = helper.PixelMap(pixels, PianoPixelMap.key_15_pixel_map, individual_pixels=True)
    key16map = helper.PixelMap(pixels, PianoPixelMap.key_16_pixel_map, individual_pixels=True)
    key17map = helper.PixelMap(pixels, PianoPixelMap.key_17_pixel_map, individual_pixels=True)
    key18map = helper.PixelMap(pixels, PianoPixelMap.key_18_pixel_map, individual_pixels=True)
    key19map = helper.PixelMap(pixels, PianoPixelMap.key_19_pixel_map, individual_pixels=True)
    key20map = helper.PixelMap(pixels, PianoPixelMap.key_20_pixel_map, individual_pixels=True)
    key21map = helper.PixelMap(pixels, PianoPixelMap.key_21_pixel_map, individual_pixels=True)
    key22map = helper.PixelMap(pixels, PianoPixelMap.key_22_pixel_map, individual_pixels=True)
    key23map = helper.PixelMap(pixels, PianoPixelMap.key_23_pixel_map, individual_pixels=True)
    key24map = helper.PixelMap(pixels, PianoPixelMap.key_24_pixel_map, individual_pixels=True)

    key_1 = Key(Button(4, hold_time = 0.1), Cn4, key1map)
    key_3 = Key(Button(3, hold_time = 0.1), Dn4, key3map)
    key_5 = Key(Button(2, hold_time = 0.1), En4, key5map)
    key_6 = Key(Button(14, hold_time = 0.1), Fn4, key6map)
    key_8 = Key(Button(15, hold_time = 0.1), Gn4, key8map)
    key_10 = Key(Button(23, hold_time = 0.1), An4, key10map)
    key_12 = Key(Button(24, hold_time = 0.1), Bn4, key12map)
    
    key_2 = Key(Button(17, hold_time = 0.1), Cs4, key2map)
    key_4 = Key(Button(22, hold_time = 0.1), Ds4, key4map)
    key_7 = Key(Button(10, hold_time = 0.1), Fs4, key7map)
    key_9 = Key(Button(9, hold_time = 0.1), Gs4, key9map)
    key_11 = Key(Button(11, hold_time = 0.1), As4, key11map)

    key_13 = Key(Button(21, hold_time = 0.1), Cn5, key13map)
    key_15 = Key(Button(20, hold_time = 0.1), Dn5, key15map)
    key_17 = Key(Button(16, hold_time = 0.1), En5, key17map)
    key_18 = Key(Button(12, hold_time = 0.1), Fn5, key18map)
    key_20 = Key(Button(1, hold_time = 0.1), Gn5, key20map)
    key_22 = Key(Button(25, hold_time = 0.1), An5, key22map)
    key_24 = Key(Button(26, hold_time = 0.1), Bn5, key24map)

    key_14 = Key(Button(0, hold_time = 0.1), Cs5, key14map)
    key_16 = Key(Button(5, hold_time = 0.1), Ds5, key16map)
    key_19 = Key(Button(6, hold_time = 0.1), Fs5, key19map)
    key_21 = Key(Button(13, hold_time = 0.1), Gs5, key21map)
    key_23 = Key(Button(19, hold_time = 0.1), As5, key23map)
    
    #unactive colors for Sharps
    black_maybe = (52, 52, 52)
    key_2 = setUnactiveColour(black_maybe)
    key_4 = setUnactiveColour(black_maybe)
    key_7 = setUnactiveColour(black_maybe)
    key_9 = setUnactiveColour(black_maybe)
    key_11 = setUnactiveColour(black_maybe)

    key_14 = setUnactiveColour(black_maybe)
    key_16 = setUnactiveColour(black_maybe)
    key_19 = setUnactiveColour(black_maybe)
    key_21 = setUnactiveColour(black_maybe)
    key_23 = setUnactiveColour(black_maybe)

    # active colors 
    key_1.setActiveColour(RED)
    key_2.setActiveColour(AMBER)
    key_3.setActiveColour(ORANGE)
    key_4.setActiveColour(YELLOW)
    key_5.setActiveColour(GREEN)
    key_6.setActiveColour(JADE)
    key_7.setActiveColour(TEAL)
    key_8.setActiveColour(CYAN)
    key_9.setActiveColour(BLUE)
    key_10.setActiveColour(PURPLE)
    key_11.setActiveColour(PINK)
    key_12.setActiveColour(MAGENTA)

    key_13.setActiveColour(RED)
    key_14.setActiveColour(AMBER)
    key_15.setActiveColour(ORANGE)
    key_16.setActiveColour(YELLOW)
    key_17.setActiveColour(GREEN)
    key_18.setActiveColour(JADE)
    key_19.setActiveColour(TEAL)
    key_20.setActiveColour(CYAN)
    key_21.setActiveColour(BLUE)
    key_22.setActiveColour(PURPLE)
    key_23.setActiveColour(PINK)
    key_24.setActiveColour(MAGENTA)
    
    piano = Piano()

    """
    piano.addKey(key_Cn2)
    piano.addKey(key_Cs2)
    piano.addKey(key_Dn2)
    piano.addKey(key_Ds2)
    piano.addKey(key_En2)
    piano.addKey(key_Fn2)
    piano.addKey(key_Fs2)
    piano.addKey(key_Gn2)
    piano.addKey(key_Gs2)
    piano.addKey(key_An2)
    piano.addKey(key_As2)
    piano.addKey(key_Bn2)
    """
    piano.addKey(key_1)
    piano.addKey(key_2)
    piano.addKey(key_3)
    piano.addKey(key_4)
    piano.addKey(key_5)
    piano.addKey(key_6)
    piano.addKey(key_7)
    piano.addKey(key_8)
    piano.addKey(key_9)
    piano.addKey(key_10)
    piano.addKey(key_11)
    piano.addKey(key_12)

    piano.addKey(key_13)
    piano.addKey(key_14)
    piano.addKey(key_15)
    piano.addKey(key_16)
    piano.addKey(key_17)
    piano.addKey(key_18)
    piano.addKey(key_19)
    piano.addKey(key_20)
    piano.addKey(key_21)
    piano.addKey(key_22)
    piano.addKey(key_23)
    piano.addKey(key_24)

    piano.addNotes([Cn2,Cs2,Dn2,Ds2,En2,Fn2,Fs2,Gn2,Gs2,An2,As2,Bn2])
    piano.addNotes([Cn3,Cs3,Dn3,Ds3,En3,Fn3,Fs3,Gn3,Gs3,An3,As3,Bn3])
    piano.addNotes([Cn4,Cs4,Dn4,Ds4,En4,Fn4,Fs4,Gn4,Gs4,An4,As4,Bn4])
    piano.addNotes([Cn5,Cs5,Dn5,Ds5,En5,Fn5,Fs5,Gn5,Gs5,An5,As5,Bn5])
    piano.addNotes([Cn6,Cs6,Dn6,Ds6])
    
    while(1):
        print("What game would you like to play:")
        print("\nOptions are:")
        print("\t1 -> FREE PLAY MODE")
        print("\t2 -> PLAY MARY HAD A LITTLE LAMB")
        print("\t3 -> PLAY C Scale")
        print("\t4 -> PLAY Cheers")
        print("\t5 -> PLAY Scale")
        print("\t6 -> PLAY Mario")
        print("\t7 -> SET scale")
        print("\t0 -> END THE PROGRAM")

        game = int(input())
        
        if game == 1: 
            print("\nEntering FREE PLAY MODE")
            """
            time_old = time.perf_counter()
            while(True):
                time_taken = time.perf_counter() - time_old
                print("Time: ", time_taken)
                piano.loopKeys()
                time_old = time_taken
            """
            piano.loopKeys(True)
            print("User input to stop keys")
            wait = input()
            piano.loopKeys(False)
                
        if game == 2: 
            print("\n Play Mary Had a little lamb")
            piano.parseSong("mary.txt")
            
        if game == 3: 
            print("\n Play CMajor")
            piano.parseSong("cmajor.txt")

        if game == 4: 
            print("\n Play Cheers")
            piano.parseSong("cheers.txt")

        if game == 5: 
            print("\n Play Scale")
            piano.parseSong("scale.txt")

        if game == 6: 
            print("\n Play Mario")
            piano.parseSong("mario.txt")

        if game == 7: 
            print("\n Changing Scale")
            print("User input to set scale:")
            scale_select = int(input())
            piano.setScale(scale_select)
            
        elif game == 0:
            print("\nDecision to end the progam")
            break;
        else: 
            print("\nInvalid Input!!! Try again :)")
            
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

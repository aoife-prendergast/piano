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

from piano_key_25 import Key 
from piano_key_25 import Piano
from piano_key_25 import Note
import pygame
from pygame import mixer
import time
import random
import simpleaudio
from gpiozero import *
from pathlib import Path
import RPi.GPIO as GPIO

from adafruit_led_animation import helper
from adafruit_led_animation.color import *
import board
import neopixel
from neopixel import NeoPixel
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.sequence import AnimationSequence

import digitalio
from pixel_mapping import PianoPixelMap

import mido
import rtmidi


def main(args):
    
    #pygame.init()
    #pygame.mixer.init(44100, -16,2,2048)

    # print(pygame.mixer.get_init())
    
    #the sounds 
    Cn2 = Note("Cn2",36)
    Cs2 = Note("C#2",37)
    Dn2 = Note("Dn2",38)
    Ds2 = Note("D#2",39)
    En2 = Note("En2",40)
    Fn2 = Note("Fn2",41)
    Fs2 = Note("F#2",42)
    Gn2 = Note("Gn2",43)
    Gs2 = Note("G#2",44)
    An2 = Note("An2",45)
    As2 = Note("A#2",46)
    Bn2 = Note("Bn2",47)
    Cn3 = Note("Cn3",48)
    Cs3 = Note("C#3",49)
    Dn3 = Note("Dn3",50)
    Ds3 = Note("D#3",51)
    En3 = Note("En3",52)
    Fn3 = Note("Fn3",53)
    Fs3 = Note("F#3",54)
    Gn3 = Note("Gn3",55)
    Gs3 = Note("G#3",56)
    An3 = Note("An3",57)
    As3 = Note("A#3",58)
    Bn3 = Note("Bn3",59)
    Cn4 = Note("Cn4",60)
    Cs4 = Note("C#4",61)
    Dn4 = Note("Dn4",62)
    Ds4 = Note("D#4",63)
    En4 = Note("En4",64)
    Fn4 = Note("Fn4",65)
    Fs4 = Note("F#4",66)
    Gn4 = Note("Gn4",67)
    Gs4 = Note("G#4",68)
    An4 = Note("An4",69)
    As4 = Note("A#4",70)
    Bn4 = Note("Bn4",71)
    Cn5 = Note("Cn5",71)
    Cs5 = Note("C#5",73)
    Dn5 = Note("Dn5",74)
    Ds5 = Note("D#5",75)
    En5 = Note("En5",76)
    Fn5 = Note("Fn5",77)
    Fs5 = Note("F#5",78)
    Gn5 = Note("Gn5",79)
    Gs5 = Note("G#5",80)
    An5 = Note("An5",81)
    As5 = Note("A#5",82)
    Bn5 = Note("Bn5",83)
    Cn6 = Note("Cn6",84)
    Cs6 = Note("C#6",85)
    Dn6 = Note("Dn6",86)
    Ds6 = Note("D#6",87)

    pixel_pin = board.D18
    pixel_num = 2245
    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=1, auto_write=False)

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


    key_1 =  Key(Cn3, key1map)
    key_3 =  Key(Dn3, key3map)
    key_5 =  Key(En3, key5map)
    key_6 =  Key(Fn3, key6map)
    key_8 =  Key(Gn3, key8map)
    key_10 = Key(An3, key10map)
    key_12 = Key(Bn3, key12map)
    
    key_2 =  Key(Cs3, key2map)
    key_4 =  Key(Ds3, key4map)
    key_7 =  Key(Fs3, key7map)
    key_9 =  Key(Gs3, key9map)
    key_11 = Key(As3, key11map)
    
    
    key_13 = Key(Cn4, key13map)
    key_15 = Key(Dn4, key15map)
    key_17 = Key(En4, key17map)
    key_18 = Key(Fn4, key18map)
    key_20 = Key(Gn4, key20map)
    key_22 = Key(An4, key22map)
    key_24 = Key(Bn4, key24map)

    key_14 = Key(Cs4, key14map)
    key_16 = Key(Ds4, key16map)
    key_19 = Key(Fs4, key19map)
    key_21 = Key(Gs4, key21map)
    key_23 = Key(As4, key23map)
    
    #unactive colors for Sharps
    sharp_default = (255,0,0)
    key_2.setUnactiveColour(sharp_default)
    key_4.setUnactiveColour(sharp_default)
    key_7.setUnactiveColour(sharp_default)
    key_9.setUnactiveColour(sharp_default)
    key_11.setUnactiveColour(sharp_default)

    key_14.setUnactiveColour(sharp_default)
    key_16.setUnactiveColour(sharp_default)
    key_19.setUnactiveColour(sharp_default)
    key_21.setUnactiveColour(sharp_default)
    key_23.setUnactiveColour(sharp_default)

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

    piano.resetLights()
    
    while(1):
        print("What game would you like to play:")
        print("\nOptions are:")
        print("\t1 -> FREE PLAY MODE")
        print("\t2 -> PLAY Taylor")
        print("\t3 -> PLAY Deck the Halls")
        print("\t4 -> SET scale")
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

        elif game == 2: 
            print("\n ")
            print("Time to play taylor:")
            midiSong = 'midi_songs/Taylor Swift - Blank Space - Pianoitall.mid'
            piano.parseSongMidi(midiSong)

        elif game == 3: 
            print("\n ")
            midiSong = 'midi_songs/Deckthehalls1H.mid'
            print("Time to play Deck the halls:")
            piano.parseSongMidi(midiSong)
            
        elif game == 4: 
            print("\n Changing Scale")
            print("User input to set scale:")
            scale_select = int(input())
            piano.setScale(scale_select)

        elif game == 5: 
            print("\n ")
            pathlist = Path("midi_songs/").rglob('*.mid')

            print("\What song would you like to play:")

            song = int(input())
            count = 0
            for path in pathlist:
                if count == song: 
                    val = path
                    break;
                count = count + 1

            midiSong = str(val)
            print(midiSong)
            print("Time to play" + midiSong)
            piano.parseSongMidi(midiSong)


            
        elif game == 0:
            print("\nDecision to end the progam")
            break;
        else: 
            print("\nInvalid Input!!! Try again :)")
            
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

import time
import rtmidi

midiout = rtmidi.MidiOut()


available_ports = midiout.get_ports()

for i in available_ports:
    print(i)

midiout.open_port(3)

print("waiting for input")
user = input() 

with midiout:
    print("Hi")
    while(1):
        print("Hi")
        note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        midiout.send_message(note_on)
        time.sleep(2)
        midiout.send_message(note_off)
        time.sleep(2)

del midiout
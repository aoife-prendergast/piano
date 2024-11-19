import mido
import rtmidi

mid = mido.MidiFile('midi_songs/coldplay-clocks.mid')
delay_constant = 1

port = mido.open_input('xyz', virtual=True)

print(mido.get_output_names())


midiout = mido.open_output('xyz:xyz 129:0')


for msg in mid.play():
    found = False
    
    print(msg)
    if(msg.channel == 0 or msg.channel == 1):
    # if(True):
        midiout.send(msg)

    """
    if(msg.type == 'note_on'):
        if(msg.velocity > 0):
            for key in keys:
                if msg.note == key.getNote().getMidiNumber():
                    print("LIGHT KEY")
                    found = True
                    #key.playSoundSong()
                # we still want to play the note even if it istn't currently active for a key
                if not found: 
                    for note in self.notes:
                        if msg.note == note.getMidiNumber():
                            #print("note found")
                            found = True
                            #note.playSound()
                if not found:
                    print(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NOTE NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" )
        
    #if(msg.time > 0):
        #time.sleep(msg.time * delay_constant)
    """


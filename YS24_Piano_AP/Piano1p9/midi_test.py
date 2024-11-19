import mido

mid = mido.MidiFile('Taylor Swift - Blank Space - Pianoitall.mid')
delay_constant = 1
for msg in mid.play():
    found = False
    print(msg)
    if( msg.velocity >= 0 and msg.type = 'note_on'):
        for key in self.keys:
            if msg.note == key.getNote().getMidiNumber():
                print("note found")
                found = True
                key.playSoundSong()
            # we still want to play the note even if it istn't currently active for a key
            if not found: 
                for note in self.notes:
                    if msg.note == note.getMidiNumber():
                        print("note found")
                        found = True
                        note.playSound()
            if not found:
                print(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NOTE NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" )
    
    if(msg.time > 0):
        time.sleep(msg.time * delay_constant)

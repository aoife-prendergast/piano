import os
import string
from pathlib import Path

def print_filenames(directory_path, file):

    print("here")
    songs = list(Path(directory_path).glob('*.mid'))
    songs.sort()

    print(len(songs))

    for i, song in enumerate(songs):
        try:
            to_print = f"Number: {i}, Song: {song.name}"
        except ValueError:
            to_print = "Something wrong with the file name"
            continue

        print(to_print)
        file.write(to_print + "\n")

# Specify the file name
file_name = "midiFiles_selectFew.txt"
directory_path = "C:/git/piano_2025/YS24_Piano_AP/midi_songs/SelectFew/"  # Replace with the target directory path

opening = "Files... Option 53"

# Create and open the file in write mode
with open(file_name, "w") as file:
    # Write the string to the file
    file.write(opening + "\n")

    print_filenames(directory_path, file)
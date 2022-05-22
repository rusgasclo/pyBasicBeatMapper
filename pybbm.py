
print("Please pick a file to map.")

#open file picker
import tkinter as tk
from tkinter import filedialog  
root = tk.Tk()
root.withdraw()
source_file = filedialog.askopenfilename(    
    title="Select a File",
    filetypes=(
        ("All Files", "*.*"),
        ("MP3 Files", "*.mp3"),
        ("OGG Files", "*.ogg"),
        ("Wav Files", "*.wav*"),
    )
)

print(source_file)
  
bpm = input("Enter BPM if known - BPM: ")

#check if bpm is numeric
try:
    float(bpm)
except ValueError:
    #call function to get bpm
    from bbm_functions import get_bpm_from_file
    bpm = get_bpm_from_file(source_file)

bpm = float(bpm)        
if bpm == 0.0:
    #call function to get bpm
    from bbm_functions import get_bpm_from_file
    bpm = get_bpm_from_file(source_file)
else:
    print("BPM: {:.2f}" .format(bpm))

from pydub import AudioSegment, silence, effects  

audio_file = AudioSegment.from_file(source_file)

#check for hot start
audio_starts = silence.detect_leading_silence(audio_file)
expected_start = (60000/bpm) * 4

if audio_starts < expected_start:
    print("Hot start detected, adding delay...")
    audio_file = AudioSegment.silent(duration=expected_start - audio_starts) + audio_file

#split audio file into left and right channels
mono = audio_file.split_to_mono()
left_channel = effects.normalize(mono[0])
right_channel = effects.normalize(mono[1])

#get loudness of left and right channels
left_loudness = left_channel.dBFS
right_loudness = right_channel.dBFS

print("Creating Notes...")
from bbm_functions import create_notes
notes = []
notes.extend(create_notes(left_channel, bpm, left_loudness, 1))
notes.extend(create_notes(right_channel, bpm, right_loudness, 2))

print(str(len(notes)) + " Notes")
print("{:.2f} Notes per second".format(len(notes) / audio_file.duration_seconds))

#ask if they want to add walls to the map
obstacles = []
add_walls = input("Add walls to map? (y/n): ")
if add_walls == "y":
    print("Creating walls...")
    from bbm_functions import create_walls
    obstacles.extend(create_walls(left_channel, bpm, left_loudness, 0))
    obstacles.extend(create_walls(right_channel, bpm, right_loudness, 3))
    print(str(len(obstacles)) + " Wall(s)")  

difficulty = {
    "_version": "2.2.0",
    "_customData": {"_time": 4, "_BPMChanges": [], "_bookmarks": []},
    "_events": [],
    "_notes": notes,
    "_obstacles": obstacles,
    "_waypoints": [],
}
#get metadata from audio file
from tinytag import TinyTag
tag = TinyTag.get(source_file)

#create folder for output
import os
file_path = os.path.dirname(source_file) + "/" + tag.title + "_map"
os.makedirs(file_path, exist_ok=True)

#write difficulty to file
import json
file = open(file_path + "/NormalStandard.dat", "w")
json.dump(difficulty, file, indent=4)
file.close()

info = {
    "_version": "2.0.0",
    "_songName": tag.title,
    "_songSubName": "",
    "_songAuthorName": tag.artist,
    "_levelAuthorName": "Rusga Sclo",
    "_beatsPerMinute": bpm,
    "_shuffle": 0,
    "_shufflePeriod": 0.5,
    "_previewStartTime": 12,
    "_previewDuration": 10,
    "_songFilename": "song.ogg",
    "_coverImageFilename": "cover.jpg",
    "_environmentName": "DefaultEnvironment",
    "_songTimeOffset": 0,
    "_customData": {
        "_contributors": [],
        "_editors": {"MMA2": {"version": "4.8.2"}, "_lastEditedBy": "MMA2"},
    },
    "_difficultyBeatmapSets": [
        {
            "_beatmapCharacteristicName": "Standard",
            "_difficultyBeatmaps": [
                {
                    "_difficulty": "Normal",
                    "_difficultyRank": 1,
                    "_beatmapFilename": "NormalStandard.dat",
                    "_noteJumpMovementSpeed": 12,
                    "_noteJumpStartBeatOffset": 0,
                    "_customData": {
                        "_editorOffset": 0,
                        "_editorOldOffset": 0,
                        "_warnings": [],
                        "_information": [],
                        "_suggestions": [],
                        "_requirements": [],
                    },
                }
            ],
        }
    ],
}

#write info to file
file = open(file_path + "/info.dat", "w")
json.dump(info, file, indent=4)
file.close()

#convert audio file to ogg
print("Converting audio file to ogg...")
audio_file.export(file_path + "/song.ogg", format="ogg", bitrate="192k", tags={"title": tag.title, "artist": tag.artist})
print ("Done!")

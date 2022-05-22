
Hi, Thanks for your interest in Basic Beat Mapper. 

This app is designed to create a map for Beat Saber from a file and works with mp3, ogg and wav files.

The intention is to suggest where notes should be placed, it's up to you to adjust block possitions and cut direction.
All notes are dot notes and are placed in the inner two columns on the bottom row based on beats detected in the left and right audio channels, this app will work with mono files but the notes will be mirrored.
Maps will be barely playable, maps produced by this app should not be uploaded to beatsaver without major editing.
This app will only output "normal" difficulty, actual difficulty will vary based on the number of notes in your song.
If you choose to add walls they will be added in the outer two columns so they will not add to difficulty, again these are just suggested placements, alter them however you wish.


About Me:
I am an amature coder in Python, I like Beat Saber and I know nothing about music theory.

FAQ:
Can I edit maps with this app?
No, the app just places notes in time with beats in a song, you should use a map editor to alter maps created by this app.

What if I don't know what the BPM of my song is?
The app will calculate the BPM for you. Entering an incorrect BPM can result in odd note placement do this at your own risk or for your own amusement.

Why are there beats missing / extra beats?
The thesholds for beats are based off the normalized loudness of a song and the bpm, if you know of a way to make this more accurate I am open to suggetions, I don't know anythig about music theory. 

Why use pydub and librosa?
I found pydub easy to use for most of the things I wanted to do except for beat detection which did not seem very acurate, librosa comes across as more complex to me but beat detection is simmple to use and accurate.

Why is there no GUI?
I'm a programmer not an artist. I feel like it doesn't really need one, this takes a file and outputs a map, there are a few good map viewers/editors out there. 





def get_bpm_from_file(source_file):
    print("Getting BPM from file please wait...")
    import librosa
    y, sr = librosa.load(source_file)
    bpm = librosa.beat.tempo(y=y, sr=sr)
    return float(bpm)


def create_walls(audio, bpm, loudness, column):
    #create list of silences in both channels, drop first and last to remove intro and outro
    from pydub.silence import detect_nonsilent 
    silences = detect_nonsilent(
            audio, 
            min_silence_len=int(bpm * 4), 
            silence_thresh=loudness * 1.5, 
            seek_step=int(bpm * 4)
            )
    silences.pop(0)
    silences.pop()

    # convert silences into walls, left "_lineIndex":0 right "_lineIndex":3
    obstacles_temp = []
    for i in silences:
        obsticle = {
            "_time": i[0] / (60000 / bpm),
            "_lineIndex": column,
            "_type": 0,
            "_duration": (i[1] - i[0]) / (60000 / bpm),
            "_width": 1,
        }
        obstacles_temp.append(obsticle)

    #obstacles_temp = obstacles_temp[0:-1]
    return obstacles_temp

def create_notes(audio, bpm, loudness, column):
    from pydub.silence import detect_nonsilent 
    beats = detect_nonsilent(
        audio,
        min_silence_len=int(bpm / 2),
        silence_thresh=loudness,
        seek_step=int(bpm / 2),
    )

    notes_temp = []
    for i in beats:
        note = {
            "_time": i[0] / (60000 / bpm),
            "_lineIndex": column,
            "_lineLayer": 0,
            "_type": 0,
            "_cutDirection": 8,
            }
        notes_temp.append(note)
    return notes_temp

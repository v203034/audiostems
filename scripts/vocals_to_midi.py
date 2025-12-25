# scripts/vocals_to_midi.py
import librosa
import pretty_midi

def vocals_to_midi(vocals_path, midi_path):
    y, sr = librosa.load(vocals_path, sr=None)
    # Estimate pitches
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)

    # Simplified: take the strongest pitch per frame
    for i in range(pitches.shape[1]):
        index = magnitudes[:, i].argmax()
        pitch = pitches[index, i]
        if pitch > 0:
            note_number = librosa.hz_to_midi(pitch)
            note = pretty_midi.Note(
                velocity=100, pitch=int(note_number),
                start=i*512/sr, end=(i+1)*512/sr
            )
            piano.notes.append(note)

    midi.instruments.append(piano)
    midi.write(midi_path)

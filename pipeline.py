from scripts.separate_stems import separate
from scripts.refine_drums import refine_drums
from scripts.vocals_to_midi import vocals_to_midi
from scripts.align_lyrics import align_lyrics
import os

INPUT = "data/input/song.wav"
OUT = "data/output"

os.makedirs(f"{OUT}/stems", exist_ok=True)
os.makedirs(f"{OUT}/drums", exist_ok=True)

# 1️⃣ Demucs stem separation
separate(INPUT, f"{OUT}/stems")

# 2️⃣ Drum refinement
refine_drums(f"{OUT}/stems/drums.wav", f"{OUT}/drums")

# 3️⃣ Extract MIDI from vocals
vocals_to_midi(f"{OUT}/stems/vocals.wav", f"{OUT}/vocals.mid")

# 4️⃣ Optional: lyrics alignment
if os.path.exists("data/input/lyrics.txt"):
    align_lyrics(
        f"{OUT}/stems/vocals.wav",
        "data/input/lyrics.txt",
        f"{OUT}/lyrics.json"
    )

# scripts/separate_stems.py
from demucs.apply import apply_model
from demucs.pretrained import get_model
import torch
import torchaudio
import os

def separate(input_path, output_dir):
    """
    Separate audio into stems (vocals, drums, bass, other) using Demucs.
    Saves WAV files in output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load model
    model = get_model('htdemucs')
    model.eval()

    # Load audio
    wav, sr = torchaudio.load(input_path)
    wav = wav.unsqueeze(0)  # batch dim

    # Apply model
    with torch.no_grad():
        sources = apply_model(model, wav, split=True, progress=True)
    sources = sources[0]  # remove batch dim

    # Map: vocals, drums, bass, other
    stems = {
        'vocals': sources[3],
        'drums': sources[0] + sources[1] + sources[2],  # sum others
        'bass': sources[1],
        'other': sources[2]
    }

    # Save stems
    for name, tensor in stems.items():
        torchaudio.save(os.path.join(output_dir, f"{name}.wav"), tensor, sr)

import os
import soundfile as sf
import numpy as np
import librosa

# Folder with your audio files
files = ["add_coffee.wav", "add_two_tea.wav", "checkout.wav"]

for file in files:
    data, samplerate = sf.read(file)

    # Resample to 16000 Hz
    if samplerate != 16000:
        data = librosa.resample(data.T, orig_sr=samplerate, target_sr=16000)
        data = data.T
        samplerate = 16000

    # Convert stereo to mono
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Save as PCM 16-bit mono, 16kHz
    sf.write(file, data, samplerate, subtype='PCM_16')
    print(f"✅ Converted {file} -> mono PCM 16kHz")

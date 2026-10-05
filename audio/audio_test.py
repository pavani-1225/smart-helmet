import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Select microphone and speaker
sd.default.device = (1, 3)

# Recording settings
sample_rate = 44100
duration = 5

print("Start speaking...")

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32"
)

sd.wait()

print("Recording finished!")

# Check audio level
print("Maximum:", np.max(np.abs(recording)))
print("Mean:", np.mean(np.abs(recording)))

# Save recording
write("test_voice.wav", sample_rate, recording)

print("Audio saved as test_voice.wav")

# Play recording
print("Playing recording...")
sd.play(recording, sample_rate)
sd.wait()

print("Done!")
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import stft, istft


# -----------------------------
# Audio settings
# -----------------------------

sd.default.device = (1, 3)

sample_rate = 44100
duration = 5

print("Start speaking...")
print("Keep the first 1 second relatively quiet for noise estimation.")


# -----------------------------
# Record audio
# -----------------------------

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32"
)

sd.wait()

print("Recording finished!")


# Convert stereo-like shape (N, 1) to 1D
audio = recording[:, 0]


# -----------------------------
# Save original recording
# -----------------------------

write("original_voice.wav", sample_rate, audio)

print("Original audio saved as original_voice.wav")


# -----------------------------
# Analyze audio using STFT
# -----------------------------

frequencies, times, Zxx = stft(
    audio,
    fs=sample_rate,
    nperseg=1024,
    noverlap=512
)

magnitude = np.abs(Zxx)
phase = np.angle(Zxx)


# -----------------------------
# Estimate background noise
# -----------------------------

noise_frames = int(1.0 / (times[1] - times[0]))

noise_profile = np.mean(
    magnitude[:, :noise_frames],
    axis=1,
    keepdims=True
)


# -----------------------------
# Noise reduction
# -----------------------------

threshold = 1.5 * noise_profile

cleaned_magnitude = np.where(
    magnitude > threshold,
    magnitude - noise_profile,
    0
)


# Prevent negative values
cleaned_magnitude = np.maximum(cleaned_magnitude, 0)


# -----------------------------
# Reconstruct audio
# -----------------------------

cleaned_spectrum = (
    cleaned_magnitude * np.exp(1j * phase)
)

_, cleaned_audio = istft(
    cleaned_spectrum,
    fs=sample_rate,
    nperseg=1024,
    noverlap=512
)


# -----------------------------
# Normalize audio
# -----------------------------

cleaned_audio = cleaned_audio / (
    np.max(np.abs(cleaned_audio)) + 1e-8
)

cleaned_audio = cleaned_audio.astype(np.float32)


# -----------------------------
# Save processed audio
# -----------------------------

write(
    "cleaned_voice.wav",
    sample_rate,
    cleaned_audio
)

print("Cleaned audio saved as cleaned_voice.wav")


# -----------------------------
# Play cleaned audio
# -----------------------------

print("Playing cleaned audio...")

sd.play(
    cleaned_audio,
    sample_rate
)

sd.wait()

print("Noise reduction processing completed!")
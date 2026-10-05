import numpy as np
from scipy.io.wavfile import read


# -----------------------------
# Load original audio
# -----------------------------

sample_rate_original, original_audio = read("original_voice.wav")
original_audio = original_audio.astype(np.float32)


# -----------------------------
# Load cleaned audio
# -----------------------------

sample_rate_cleaned, cleaned_audio = read("cleaned_voice.wav")
cleaned_audio = cleaned_audio.astype(np.float32)


# -----------------------------
# Use common length
# -----------------------------

common_length = min(
    len(original_audio),
    len(cleaned_audio)
)

original_audio = original_audio[:common_length]
cleaned_audio = cleaned_audio[:common_length]


# -----------------------------
# First 1 second = noise section
# Remaining audio = speech section
# -----------------------------

noise_samples = min(
    sample_rate_original,
    common_length
)

original_noise = original_audio[:noise_samples]
cleaned_noise = cleaned_audio[:noise_samples]

original_speech = original_audio[noise_samples:]
cleaned_speech = cleaned_audio[noise_samples:]


# -----------------------------
# RMS calculation
# -----------------------------

def calculate_rms(signal):
    return np.sqrt(np.mean(signal ** 2))


original_noise_rms = calculate_rms(original_noise)
cleaned_noise_rms = calculate_rms(cleaned_noise)

original_speech_rms = calculate_rms(original_speech)
cleaned_speech_rms = calculate_rms(cleaned_speech)


# -----------------------------
# Estimate SNR
# -----------------------------

epsilon = 1e-12

snr_before = 20 * np.log10(
    (original_speech_rms + epsilon) /
    (original_noise_rms + epsilon)
)

snr_after = 20 * np.log10(
    (cleaned_speech_rms + epsilon) /
    (cleaned_noise_rms + epsilon)
)

snr_improvement = snr_after - snr_before


# -----------------------------
# Display results
# -----------------------------

print("\n========================================")
print("      SMART HELMET AUDIO ANALYSIS")
print("========================================")

print("\nSample Rate:")
print(sample_rate_original, "Hz")

print("\n--- Noise RMS ---")
print("Before noise reduction:", original_noise_rms)
print("After noise reduction :", cleaned_noise_rms)

print("\n--- Speech RMS ---")
print("Before noise reduction:", original_speech_rms)
print("After noise reduction :", cleaned_speech_rms)

print("\n--- SNR Estimate ---")
print("Before:", snr_before, "dB")
print("After :", snr_after, "dB")

print("\n--- SNR Improvement ---")
print(snr_improvement, "dB")

print("\n========================================")
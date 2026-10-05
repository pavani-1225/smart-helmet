import sounddevice as sd
import numpy as np
from scipy.signal import stft, istft


# ==========================================
# SMART HELMET
# AUDIO PERFORMANCE TEST
# ==========================================

sd.default.device = (1, 3)

SAMPLE_RATE = 44100
DURATION = 5

print("\n========================================")
print(" SMART HELMET AUDIO PERFORMANCE TEST")
print("========================================")

print("\nYou will record for 5 seconds.")
print("Keep the first 1 second relatively quiet.")
print("Then speak normally for the remaining 4 seconds.")

input("\nPress ENTER when you are ready...")

print("\nRecording...")

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

print("Recording completed.")


# ==========================================
# Convert to 1D
# ==========================================

original = recording[:, 0]


# ==========================================
# STFT
# ==========================================

frequencies, times, spectrum = stft(
    original,
    fs=SAMPLE_RATE,
    nperseg=1024,
    noverlap=512
)

magnitude = np.abs(spectrum)
phase = np.angle(spectrum)


# ==========================================
# Noise estimation
# ==========================================

noise_frames = int(
    1.0 / (times[1] - times[0])
)

noise_profile = np.mean(
    magnitude[:, :noise_frames],
    axis=1,
    keepdims=True
)


# ==========================================
# Noise reduction
# ==========================================

threshold = 1.5 * noise_profile

cleaned_magnitude = np.where(
    magnitude > threshold,
    magnitude - noise_profile,
    0
)

cleaned_magnitude = np.maximum(
    cleaned_magnitude,
    0
)


# ==========================================
# Reconstruct
# ==========================================

cleaned_spectrum = (
    cleaned_magnitude *
    np.exp(1j * phase)
)

_, cleaned = istft(
    cleaned_spectrum,
    fs=SAMPLE_RATE,
    nperseg=1024,
    noverlap=512
)


# ==========================================
# Match lengths
# ==========================================

common_length = min(
    len(original),
    len(cleaned)
)

original = original[:common_length]
cleaned = cleaned[:common_length]


# ==========================================
# RMS function
# ==========================================

def rms(signal):

    return np.sqrt(
        np.mean(signal ** 2)
    )


# ==========================================
# Separate noise and speech sections
# ==========================================

noise_samples = min(
    SAMPLE_RATE,
    common_length
)

original_noise = original[:noise_samples]
cleaned_noise = cleaned[:noise_samples]

original_speech = original[noise_samples:]
cleaned_speech = cleaned[noise_samples:]


# ==========================================
# Calculate RMS
# ==========================================

original_noise_rms = rms(
    original_noise
)

cleaned_noise_rms = rms(
    cleaned_noise
)

original_speech_rms = rms(
    original_speech
)

cleaned_speech_rms = rms(
    cleaned_speech
)


# ==========================================
# Calculate SNR
# ==========================================

epsilon = 1e-12

snr_before = 20 * np.log10(
    (original_speech_rms + epsilon) /
    (original_noise_rms + epsilon)
)

snr_after = 20 * np.log10(
    (cleaned_speech_rms + epsilon) /
    (cleaned_noise_rms + epsilon)
)

snr_improvement = (
    snr_after - snr_before
)

# ==========================================
# Save and play processed audio
# ==========================================

print("\nPlaying processed audio...")

sd.play(
    cleaned,
    SAMPLE_RATE
)

sd.wait()

print("Playback completed.")


# ==========================================
# Display results
# ==========================================

print("\n========================================")
print("          TEST RESULTS")
print("========================================")

print("\nSample rate:")
print(SAMPLE_RATE, "Hz")

print("\nRecording duration:")
print(DURATION, "seconds")

print("\n--- NOISE LEVEL (RMS) ---")
print(
    "Before:",
    round(original_noise_rms, 6)
)

print(
    "After :",
    round(cleaned_noise_rms, 6)
)

print("\n--- SPEECH LEVEL (RMS) ---")
print(
    "Before:",
    round(original_speech_rms, 6)
)

print(
    "After :",
    round(cleaned_speech_rms, 6)
)

print("\n--- SNR ---")
print(
    "Before:",
    round(snr_before, 2),
    "dB"
)

print(
    "After :",
    round(snr_after, 2),
    "dB"
)

print("\n--- SNR IMPROVEMENT ---")
print(
    round(snr_improvement, 2),
    "dB"
)

print("\n========================================")
print(" Audio performance test completed.")
print("========================================")
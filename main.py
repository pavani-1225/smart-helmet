import sounddevice as sd
import numpy as np
from scipy.signal import stft, istft


# ==========================================
# SMART HELMET AUDIO PROCESSING SYSTEM
# ==========================================

# Audio configuration
sd.default.device = (1, 3)

SAMPLE_RATE = 44100
DURATION = 5


# ==========================================
# 1. RECORD AUDIO
# ==========================================

print("\n========================================")
print("       SMART HELMET AUDIO SYSTEM")
print("========================================")

print("\nStart speaking...")
print("Keep the first 1 second relatively quiet.")

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

print("Recording completed.")


# Convert to 1D signal
audio = recording[:, 0]


# ==========================================
# 2. STFT ANALYSIS
# ==========================================

print("Analyzing audio...")

frequencies, times, spectrum = stft(
    audio,
    fs=SAMPLE_RATE,
    nperseg=1024,
    noverlap=512
)

magnitude = np.abs(spectrum)
phase = np.angle(spectrum)


# ==========================================
# 3. ESTIMATE BACKGROUND NOISE
# ==========================================

print("Estimating background noise...")

noise_frames = int(
    1.0 / (times[1] - times[0])
)

noise_profile = np.mean(
    magnitude[:, :noise_frames],
    axis=1,
    keepdims=True
)


# ==========================================
# 4. NOISE REDUCTION
# ==========================================

print("Applying noise reduction...")

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
# 5. RECONSTRUCT CLEANED AUDIO
# ==========================================

cleaned_spectrum = (
    cleaned_magnitude *
    np.exp(1j * phase)
)

_, cleaned_audio = istft(
    cleaned_spectrum,
    fs=SAMPLE_RATE,
    nperseg=1024,
    noverlap=512
)


# ==========================================
# 6. NORMALIZE OUTPUT
# ==========================================

cleaned_audio = cleaned_audio / (
    np.max(np.abs(cleaned_audio)) + 1e-8
)

cleaned_audio = cleaned_audio.astype(
    np.float32
)


# ==========================================
# 7. PLAY CLEANED AUDIO
# ==========================================

print("Playing processed voice...")

sd.play(
    cleaned_audio,
    SAMPLE_RATE
)

sd.wait()


# ==========================================
# 8. SYSTEM COMPLETE
# ==========================================

print("\n========================================")
print(" Noise reduction completed successfully")
print("========================================")
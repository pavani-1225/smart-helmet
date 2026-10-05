import sounddevice as sd
import numpy as np


# ==========================================
# SMART HELMET
# REAL-TIME FREQUENCY-DOMAIN NOISE REDUCTION
# ==========================================

sd.default.device = (1, 3)

SAMPLE_RATE = 44100
CHANNELS = 1

BLOCK_SIZE = 1024
FFT_SIZE = 1024


# ==========================================
# Noise profile
# ==========================================

noise_profile = None


print("\n========================================")
print(" SMART HELMET REAL-TIME NOISE REDUCTION")
print("========================================")

print("\nKeep quiet for the first few seconds.")
print("The system will estimate background noise.")
print("Then speak normally.")
print("Press Ctrl+C to stop.\n")


# ==========================================
# Audio callback
# ==========================================

def audio_callback(indata, outdata, frames, time, status):

    global noise_profile

    if status:
        print(status)

    # Get microphone audio
    audio = indata[:, 0].copy()

    # Make sure the block has the expected size
    if len(audio) < FFT_SIZE:

        outdata[:, 0] = audio

        return

    # ======================================
    # FFT
    # ======================================

    spectrum = np.fft.rfft(audio, n=FFT_SIZE)

    magnitude = np.abs(spectrum)

    phase = np.angle(spectrum)


    # ======================================
    # Estimate background noise
    # ======================================

    if noise_profile is None:

        noise_profile = magnitude.copy()

    else:

        # Slowly update noise estimate
        noise_profile = (
            0.98 * noise_profile
            + 0.02 * magnitude
        )


    # ======================================
    # Spectral noise suppression
    # ======================================

    threshold = 1.5 * noise_profile

    cleaned_magnitude = np.where(
        magnitude > threshold,
        magnitude - noise_profile,
        0
    )


    # Prevent negative values
    cleaned_magnitude = np.maximum(
        cleaned_magnitude,
        0
    )


    # ======================================
    # Reconstruct spectrum
    # ======================================

    cleaned_spectrum = (
        cleaned_magnitude
        * np.exp(1j * phase)
    )


    # ======================================
    # Inverse FFT
    # ======================================

    cleaned_audio = np.fft.irfft(
        cleaned_spectrum,
        n=FFT_SIZE
    )


    # ======================================
    # Output
    # ======================================

    cleaned_audio = cleaned_audio.astype(
        np.float32
    )

    outdata[:, 0] = cleaned_audio[:frames]


# ==========================================
# Start real-time audio
# ==========================================

try:

    with sd.Stream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=CHANNELS,
        dtype="float32",
        callback=audio_callback
    ):

        while True:

            sd.sleep(1000)


except KeyboardInterrupt:

    print("\n========================================")
    print(" Real-time processing stopped.")
    print("========================================")


except Exception as e:

    print("\nError:", e)
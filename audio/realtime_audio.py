import sounddevice as sd
import numpy as np


# ==========================================
# SMART HELMET REAL-TIME NOISE REDUCTION
# ==========================================

sd.default.device = (1, 3)

SAMPLE_RATE = 44100
CHANNELS = 1
BLOCK_SIZE = 1024


# ==========================================
# Noise estimation
# ==========================================

noise_level = 0.01

print("\n========================================")
print(" SMART HELMET REAL-TIME NOISE REDUCTION")
print("========================================")

print("\nStarting system...")
print("Keep the environment relatively quiet for")
print("the first few seconds.")
print("Speak normally after that.")
print("Press Ctrl+C to stop.\n")


# ==========================================
# Audio callback
# ==========================================

def audio_callback(indata, outdata, frames, time, status):

    global noise_level

    if status:
        print(status)

    # Copy microphone input
    audio = indata[:, 0].copy()

    # --------------------------------------
    # Calculate current audio level
    # --------------------------------------

    current_level = np.sqrt(
        np.mean(audio ** 2)
    )

    # --------------------------------------
    # Slowly estimate background noise
    # --------------------------------------

    if current_level < noise_level * 2:

        noise_level = (
            0.95 * noise_level
            + 0.05 * current_level
        )

    # --------------------------------------
    # Simple noise suppression
    # --------------------------------------

    threshold = noise_level * 1.5

    processed = np.where(
        np.abs(audio) > threshold,
        audio,
        audio * 0.15
    )

    # --------------------------------------
    # Prevent clipping
    # --------------------------------------

    processed = np.clip(
        processed,
        -1.0,
        1.0
    )

    # Send processed audio to speaker
    outdata[:, 0] = processed


# ==========================================
# Start real-time stream
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
    print(" Real-time system stopped.")
    print("========================================")


except Exception as e:

    print("\nError:", e)
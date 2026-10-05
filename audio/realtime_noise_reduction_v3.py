import sounddevice as sd
import numpy as np


# ==========================================
# SMART HELMET
# REAL-TIME NOISE REDUCTION - V3
# Proper Overlap-Add Processing
# ==========================================

sd.default.device = (1, 3)

SAMPLE_RATE = 44100
CHANNELS = 1

FFT_SIZE = 1024
HOP_SIZE = 512


# ==========================================
# Noise profile
# ==========================================

noise_profile = None


# ==========================================
# Window
# ==========================================

window = np.hanning(FFT_SIZE)


# ==========================================
# Buffers
# ==========================================

input_buffer = np.zeros(FFT_SIZE, dtype=np.float32)

output_buffer = np.zeros(FFT_SIZE, dtype=np.float32)


# ==========================================
# Display
# ==========================================

print("\n========================================")
print(" SMART HELMET REAL-TIME NOISE REDUCTION")
print("                 V3")
print("========================================")

print("\nKeep quiet for the first few seconds.")
print("The system will estimate background noise.")
print("Then speak normally.")
print("Press Ctrl+C to stop.\n")


# ==========================================
# Audio callback
# ==========================================

def audio_callback(indata, outdata, frames, time_info, status):

    global noise_profile
    global input_buffer
    global output_buffer

    if status:
        print(status)

    audio = indata[:, 0].copy()

    # --------------------------------------
    # Shift old samples
    # --------------------------------------

    input_buffer[:-frames] = input_buffer[frames:]

    input_buffer[-frames:] = audio


    # --------------------------------------
    # Apply Hann window
    # --------------------------------------

    windowed_audio = input_buffer * window


    # --------------------------------------
    # FFT
    # --------------------------------------

    spectrum = np.fft.rfft(
        windowed_audio,
        n=FFT_SIZE
    )

    magnitude = np.abs(spectrum)
    phase = np.angle(spectrum)


    # --------------------------------------
    # Noise estimation
    # --------------------------------------

    if noise_profile is None:

        noise_profile = magnitude.copy()

    else:

        noise_profile = (
            0.995 * noise_profile
            + 0.005 * magnitude
        )


    # --------------------------------------
    # Spectral subtraction
    # --------------------------------------

    threshold = 1.5 * noise_profile

    cleaned_magnitude = np.where(
        magnitude > threshold,
        magnitude - noise_profile,
        0
    )


    # --------------------------------------
    # Prevent negative values
    # --------------------------------------

    cleaned_magnitude = np.maximum(
        cleaned_magnitude,
        0
    )


    # --------------------------------------
    # Reconstruct spectrum
    # --------------------------------------

    cleaned_spectrum = (
        cleaned_magnitude
        * np.exp(1j * phase)
    )


    # --------------------------------------
    # Inverse FFT
    # --------------------------------------

    cleaned_frame = np.fft.irfft(
        cleaned_spectrum,
        n=FFT_SIZE
    )


    # --------------------------------------
    # Apply window again
    # --------------------------------------

    cleaned_frame = (
        cleaned_frame * window
    )


    # --------------------------------------
    # Overlap-add
    # --------------------------------------

    output_buffer += cleaned_frame


    # --------------------------------------
    # Output current hop
    # --------------------------------------

    output = output_buffer[:frames].copy()


    # --------------------------------------
    # Shift output buffer
    # --------------------------------------

    output_buffer[:-frames] = output_buffer[frames:]

    output_buffer[-frames:] = 0


    # --------------------------------------
    # Prevent clipping
    # --------------------------------------

    output = np.clip(
        output,
        -1.0,
        1.0
    )


    # --------------------------------------
    # Send to speaker
    # --------------------------------------

    outdata[:, 0] = output.astype(
        np.float32
    )


# ==========================================
# Start stream
# ==========================================

try:

    with sd.Stream(
        samplerate=SAMPLE_RATE,
        blocksize=HOP_SIZE,
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
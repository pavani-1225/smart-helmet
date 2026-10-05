import sounddevice as sd
import numpy as np


# ========================================
# SMART HELMET REAL-TIME AUDIO SYSTEM
# ========================================

SAMPLE_RATE = 44100
CHANNELS = 1

FFT_SIZE = 1024
HOP_SIZE = 512

VOICE_GAIN = 2.0

noise_profile = None

window = np.hanning(FFT_SIZE)

input_buffer = np.zeros(
    FFT_SIZE,
    dtype=np.float32
)

output_buffer = np.zeros(
    FFT_SIZE,
    dtype=np.float32
)


def audio_callback(
    indata,
    outdata,
    frames,
    time_info,
    status
):

    global noise_profile
    global input_buffer
    global output_buffer

    if status:
        print(status)

    audio = indata[:, 0].copy()

    # Update input buffer
    input_buffer[:-frames] = input_buffer[frames:]
    input_buffer[-frames:] = audio

    # Apply window
    windowed_audio = input_buffer * window

    # FFT
    spectrum = np.fft.rfft(
        windowed_audio,
        n=FFT_SIZE
    )

    magnitude = np.abs(spectrum)
    phase = np.angle(spectrum)

    # Estimate background noise
    if noise_profile is None:

        noise_profile = magnitude.copy()

    else:

        noise_profile = (
            0.995 * noise_profile
            + 0.005 * magnitude
        )

    # Noise reduction
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

    # Reconstruct spectrum
    cleaned_spectrum = (
        cleaned_magnitude
        * np.exp(1j * phase)
    )

    # Inverse FFT
    cleaned_frame = np.fft.irfft(
        cleaned_spectrum,
        n=FFT_SIZE
    )

    # Apply window
    cleaned_frame = (
        cleaned_frame * window
    )

    # Increase voice level
    cleaned_frame = (
        cleaned_frame * VOICE_GAIN
    )

    # Overlap-add
    output_buffer += cleaned_frame

    output = output_buffer[:frames].copy()

    output_buffer[:-frames] = (
        output_buffer[frames:]
    )

    output_buffer[-frames:] = 0

    # Prevent clipping
    output = np.clip(
        output,
        -1.0,
        1.0
    )

    outdata[:, 0] = output.astype(
        np.float32
    )


def start_audio_processing():

    print("\n========================================")
    print(" SMART HELMET REAL-TIME AUDIO SYSTEM")
    print("========================================")

    print("\nAudio processing starting...")
    print("Noise reduction: ACTIVE")
    print("Voice enhancement: ACTIVE")
    print("Press Ctrl+C to stop.\n")

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

        print("\nAudio processing stopped.")

    except Exception as e:

        print("\nAudio processing error:")
        print(e)


# ========================================
# STANDALONE TEST
# ========================================

if __name__ == "__main__":

    start_audio_processing()
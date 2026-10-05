import time
import sounddevice as sd
import numpy as np


# ==========================================
# REAL-TIME AUDIO PERFORMANCE TEST
# ==========================================

sd.default.device = (1, 3)

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024
CHANNELS = 1

processing_times = []


print("\n========================================")
print(" SMART HELMET AUDIO PERFORMANCE TEST")
print("========================================")

block_duration_ms = (
    BLOCK_SIZE / SAMPLE_RATE
) * 1000

print("\nAudio block duration:",
      round(block_duration_ms, 2), "ms")

print("\nSpeak normally for about 10 seconds.")
print("Press Ctrl+C to stop.\n")


def audio_callback(indata, outdata, frames, time_info, status):

    if status:
        print(status)

    start_time = time.perf_counter()

    # Get audio
    audio = indata[:, 0].copy()

    # FFT
    spectrum = np.fft.rfft(
        audio,
        n=BLOCK_SIZE
    )

    magnitude = np.abs(spectrum)
    phase = np.angle(spectrum)

    # Simple noise estimate
    noise_profile = magnitude * 0.5

    # Noise suppression
    cleaned_magnitude = np.maximum(
        magnitude - noise_profile,
        0
    )

    # Reconstruct
    cleaned_spectrum = (
        cleaned_magnitude *
        np.exp(1j * phase)
    )

    cleaned_audio = np.fft.irfft(
        cleaned_spectrum,
        n=BLOCK_SIZE
    )

    cleaned_audio = cleaned_audio.astype(
        np.float32
    )

    outdata[:, 0] = cleaned_audio

    # Measure processing time
    end_time = time.perf_counter()

    processing_time_ms = (
        end_time - start_time
    ) * 1000

    processing_times.append(
        processing_time_ms
    )


try:

    with sd.Stream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=CHANNELS,
        dtype="float32",
        callback=audio_callback
    ):

        sd.sleep(10000)


except Exception as e:

    print("\nError:", e)


# ==========================================
# Results
# ==========================================

if processing_times:

    processing_times = np.array(
        processing_times
    )

    print("\n========================================")
    print(" PERFORMANCE RESULTS")
    print("========================================")

    print(
        "\nAverage processing time:",
        round(np.mean(processing_times), 3),
        "ms"
    )

    print(
        "Maximum processing time:",
        round(np.max(processing_times), 3),
        "ms"
    )

    print(
        "Audio block duration:",
        round(block_duration_ms, 3),
        "ms"
    )

    print(
        "Number of processed blocks:",
        len(processing_times)
    )

    print("\n========================================")
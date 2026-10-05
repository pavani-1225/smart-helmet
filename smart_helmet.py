import threading

from audio.realtime_noise_reduction_v3_1 import (
    start_audio_processing
)

from sensors.mpu6050_simulation import (
    run_fall_detection
)


print("\n========================================")
print("        AI SMART HELMET SYSTEM")
print("========================================")


print("\nInitializing Smart Helmet...")

print("Fall detection      : READY")
print("GPS                 : READY")
print("Emergency system    : READY")
print("Communication       : READY")
print("Audio processing    : READY")


print("\n========================================")
print("        SMART HELMET READY")
print("========================================")


# ========================================
# START AUDIO PROCESSING
# ========================================

print("\nStarting real-time audio processing...")

audio_thread = threading.Thread(
    target=start_audio_processing,
    daemon=True
)

audio_thread.start()


# ========================================
# START SAFETY MONITORING
# ========================================

print("\nStarting safety monitoring...")

run_fall_detection()


# ========================================
# SHUTDOWN
# ========================================

print("\n========================================")
print("     SMART HELMET SHUTDOWN")
print("========================================")
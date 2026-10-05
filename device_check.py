import sounddevice as sd

print("\n===== AUDIO DEVICES =====\n")

print(sd.query_devices())

print("\n===== DEFAULT DEVICE =====\n")

print(sd.default.device)
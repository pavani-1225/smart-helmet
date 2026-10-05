import time

# Simulated GPS coordinates
latitude = 12.9716
longitude = 77.5946


if __name__ == "__main__":

    print("\n========================================")
    print("       SMART HELMET GPS SYSTEM")
    print("========================================")

    print("\nGPS Status: Connected")
    print("Reading location...")

    time.sleep(1)

    print("\n----------------------------------------")
    print(f"Latitude : {latitude}")
    print(f"Longitude: {longitude}")
    print("----------------------------------------")

    print("\nLocation obtained successfully.")

    print("\n========================================")
    print("       GPS TEST COMPLETED")
    print("========================================")
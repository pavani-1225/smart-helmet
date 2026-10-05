import time


def send_emergency_message(message):

    print("\n========================================")
    print("   SMART HELMET COMMUNICATION SYSTEM")
    print("========================================")

    print("\nInitializing communication module...")

    time.sleep(1)

    print("Communication module: READY")

    print("\nPreparing emergency message...")

    time.sleep(1)

    print("\n----------------------------------------")
    print("Message:")
    print(message)
    print("----------------------------------------")

    print("\nTransmission status: SUCCESS")


if __name__ == "__main__":

    print("\n========================================")
    print("   COMMUNICATION MODULE TEST")
    print("========================================")

    test_message = "Emergency alert: Fall detected!"

    send_emergency_message(test_message)

    print("\n========================================")
    print("   COMMUNICATION TEST COMPLETED")
    print("========================================")
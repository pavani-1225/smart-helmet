from datetime import datetime
from communication.communication_simulation import send_emergency_message


def trigger_emergency(latitude=None, longitude=None):

    print("\n========================================")
    print("       EMERGENCY EVENT SYSTEM")
    print("========================================")

    current_time = datetime.now()

    print("\n🚨 EMERGENCY EVENT TRIGGERED!")

    print("\nEvent:")
    print("Fall detected")

    print("\nTime:")
    print(current_time.strftime("%Y-%m-%d %H:%M:%S"))

    print("\nLocation:")

    if latitude is not None and longitude is not None:
        print(f"Latitude : {latitude}")
        print(f"Longitude: {longitude}")
    else:
        print("GPS location unavailable")

    print("\nStatus:")
    print("Emergency alert generated")

    print("\nAction:")
    print("Emergency response required")

    # Prepare emergency communication message
    message = "Emergency alert: Fall detected!"

    if latitude is not None and longitude is not None:
        message += (
            f" Location: Latitude {latitude}, "
            f"Longitude {longitude}"
        )

    # Send emergency message
    send_emergency_message(message)

    print("\n========================================")


if __name__ == "__main__":
    trigger_emergency()
import math
import time

from safety.emergency import trigger_emergency
from sensors.gps_simulation import latitude, longitude


# ========================================
# FALL DETECTION CONFIGURATION
# ========================================

IMPACT_THRESHOLD = 2.5
FREE_FALL_THRESHOLD = 0.4
POST_IMPACT_THRESHOLD = 1.2


def calculate_acceleration(x, y, z):
    """
    Calculate total acceleration magnitude
    from X, Y and Z accelerometer readings.
    """

    return math.sqrt(
        x * x +
        y * y +
        z * z
    )


def process_acceleration(x, y, z,
                         free_fall_detected,
                         impact_detected):

    """
    Process one accelerometer reading.

    Returns:
        free_fall_detected
        impact_detected
        fall_confirmed
    """

    total_acceleration = calculate_acceleration(
        x, y, z
    )

    fall_confirmed = False

    print("\n----------------------------------------")

    print(
        f"X: {x:.2f} g | "
        f"Y: {y:.2f} g | "
        f"Z: {z:.2f} g"
    )

    print(
        f"Total acceleration: "
        f"{total_acceleration:.2f} g"
    )

    # ------------------------------------
    # STEP 1: FREE-FALL DETECTION
    # ------------------------------------

    if total_acceleration < FREE_FALL_THRESHOLD:

        free_fall_detected = True

        print("⚠ Possible free-fall detected!")

    # ------------------------------------
    # STEP 2: IMPACT DETECTION
    # ------------------------------------

    elif (
        free_fall_detected
        and total_acceleration >= IMPACT_THRESHOLD
    ):

        impact_detected = True

        print("🚨 Strong impact detected!")

        print(
            "Checking whether impact "
            "followed a free-fall..."
        )

    # ------------------------------------
    # STEP 3: POST-IMPACT CHECK
    # ------------------------------------

    elif impact_detected:

        print("Checking post-impact movement...")

        if total_acceleration < POST_IMPACT_THRESHOLD:

            print("⚠ Post-impact state detected.")

            print("🚨 FALL CONFIRMED!")

            fall_confirmed = True

            # Reset states
            free_fall_detected = False
            impact_detected = False

        else:

            print("Movement detected.")

    # ------------------------------------
    # NORMAL MOVEMENT
    # ------------------------------------

    else:

        print("Normal movement")

    return (
        free_fall_detected,
        impact_detected,
        fall_confirmed
    )


def run_fall_detection():

    print("\n========================================")
    print("   SMART HELMET FALL DETECTION TEST")
    print("========================================")

    # ------------------------------------
    # SIMULATED MPU6050 DATA
    # ------------------------------------

    test_data = [

        # Normal movement
        (0.02, 0.01, 1.00),
        (0.05, 0.02, 0.98),
        (0.10, 0.05, 1.05),

        # Free-fall
        (0.02, 0.01, 0.15),
        (0.10, 0.08, 0.20),

        # Strong impact
        (2.50, 1.80, 3.20),

        # Post-impact state
        (0.20, 0.10, 0.95),
        (0.15, 0.10, 0.90),
        (0.12, 0.08, 0.92),
    ]

    free_fall_detected = False
    impact_detected = False

    # ------------------------------------
    # PROCESS SENSOR DATA
    # ------------------------------------

    for x, y, z in test_data:

        (
            free_fall_detected,
            impact_detected,
            fall_confirmed
        ) = process_acceleration(
            x,
            y,
            z,
            free_fall_detected,
            impact_detected
        )

        # --------------------------------
        # EMERGENCY RESPONSE
        # --------------------------------

        if fall_confirmed:

            trigger_emergency(
                latitude,
                longitude
            )

        time.sleep(1)

    print("\n========================================")
    print(" Fall detection test completed.")
    print("========================================")


# ========================================
# RUN TEST ONLY WHEN EXECUTED DIRECTLY
# ========================================

if __name__ == "__main__":

    run_fall_detection()
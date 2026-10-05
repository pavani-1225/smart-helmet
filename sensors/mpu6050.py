import time
import math


# ========================================
# MPU6050 SENSOR CONFIGURATION
# ========================================

MPU6050_ADDRESS = 0x68

ACCEL_XOUT_H = 0x3B
PWR_MGMT_1 = 0x6B
ACCEL_CONFIG = 0x1C


class MPU6050:

    def __init__(self, bus_number=1):

        self.bus_number = bus_number

        try:
            import smbus2

            self.smbus2 = smbus2
            self.bus = smbus2.SMBus(bus_number)

            self.initialize_sensor()

            print("MPU6050 initialized successfully.")

        except ImportError:

            print(
                "smbus2 is not installed."
            )

            self.bus = None

        except Exception as e:

            print(
                f"MPU6050 initialization error: {e}"
            )

            self.bus = None


    # ====================================
    # SENSOR INITIALIZATION
    # ====================================

    def initialize_sensor(self):

        # Wake up MPU6050
        self.bus.write_byte_data(
            MPU6050_ADDRESS,
            PWR_MGMT_1,
            0
        )

        # Set accelerometer range to ±2g
        self.bus.write_byte_data(
            MPU6050_ADDRESS,
            ACCEL_CONFIG,
            0x00
        )


    # ====================================
    # READ 16-BIT SENSOR VALUE
    # ====================================

    def read_raw_data(self, address):

        high = self.bus.read_byte_data(
            MPU6050_ADDRESS,
            address
        )

        low = self.bus.read_byte_data(
            MPU6050_ADDRESS,
            address + 1
        )

        value = (
            (high << 8) |
            low
        )

        # Convert to signed 16-bit value
        if value >= 32768:
            value -= 65536

        return value


    # ====================================
    # READ ACCELERATION
    # ====================================

    def read_acceleration(self):

        if self.bus is None:

            raise RuntimeError(
                "MPU6050 is not connected."
            )

        raw_x = self.read_raw_data(
            ACCEL_XOUT_H
        )

        raw_y = self.read_raw_data(
            ACCEL_XOUT_H + 2
        )

        raw_z = self.read_raw_data(
            ACCEL_XOUT_H + 4
        )

        # ±2g range = 16384 LSB/g

        x = raw_x / 16384.0
        y = raw_y / 16384.0
        z = raw_z / 16384.0

        return x, y, z


    # ====================================
    # CALCULATE TOTAL ACCELERATION
    # ====================================

    def get_total_acceleration(self):

        x, y, z = self.read_acceleration()

        total = math.sqrt(
            x * x +
            y * y +
            z * z
        )

        return x, y, z, total


    # ====================================
    # CLOSE SENSOR
    # ====================================

    def close(self):

        if self.bus is not None:

            self.bus.close()


# ========================================
# REAL SENSOR TEST
# ========================================

def test_mpu6050():

    print("\n========================================")
    print("      MPU6050 SENSOR TEST")
    print("========================================")

    sensor = MPU6050()

    try:

        print("\nReading accelerometer...")
        print("Press Ctrl+C to stop.\n")

        while True:

            x, y, z, total = (
                sensor.get_total_acceleration()
            )

            print(
                f"X: {x:.2f} g | "
                f"Y: {y:.2f} g | "
                f"Z: {z:.2f} g | "
                f"Total: {total:.2f} g"
            )

            time.sleep(0.5)

    except KeyboardInterrupt:

        print("\nMPU6050 test stopped.")

    finally:

        sensor.close()


# ========================================
# RUN ONLY WHEN EXECUTED DIRECTLY
# ========================================

if __name__ == "__main__":

    test_mpu6050()
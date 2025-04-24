#!/usr/bin/env python3

import RPi.GPIO as GPIO
from datetime import datetime
import time

# ====== Config ======
PWM_PIN = 17
ITERATIONS_COUNT = 5

CALIBRATION_SCALING_FACTOR = 1
# Scaling Factor = outside air ppm / sensor output ppm
# Do this often to get a good value
# ====================

def get_sensor_data():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PWM_PIN, GPIO.IN)

    is_high = False
    t_high = t_low = None
    values = []
    iteration = 0

    try:
        while iteration < ITERATIONS_COUNT + 1:
            val = GPIO.input(PWM_PIN)

            if val and not is_high:
                is_high = True
                t_high = datetime.utcnow()

            elif not val and is_high:
                is_high = False
                t_low = datetime.utcnow()

            if t_high and t_low:
                duration = t_low - t_high
                duration_ms = int(duration.total_seconds() * 1000)  # Convert to milliseconds

                # Calculate concentration in ppm
                cppm = CALIBRATION_SCALING_FACTOR * 2000 * (duration_ms - 2) / (1004 - 4)
                values.append(cppm)

                iteration += 1
                t_high = t_low = None

            time.sleep(0.001)  # Small delay to avoid busy looping

        # Remove the first value (possibly inaccurate)
        values = values[1:]
        ppm = int(sum(values) / len(values))
        return ppm

    finally:
        GPIO.cleanup()


def main():
    ppm = get_sensor_data()
    print(f"CO2 Concentration: {ppm} ppm")


if __name__=="__main__":
    main()

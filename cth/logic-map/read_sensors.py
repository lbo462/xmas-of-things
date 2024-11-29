"""

    Simple subscription to the UPLINK topic and reads data sent by the sensors.

"""

import time
import logging
from ttn_al import get_ttn_access_layer
from topics import sensors_topic, SensorsTTNPayload
from settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL


logging.basicConfig(level=logging.INFO)


def on_sensors_data(sensors_data: SensorsTTNPayload):
    print(sensors_data)


def main():
    with get_ttn_access_layer(
        TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, sensors_topic, on_message=on_sensors_data
    ):
        time.sleep(5000)  # Listen for 500 seconds


if __name__ == "__main__":
    main()

"""

    Simple subscription to the UPLINK topic and reads data sent by the sensors.

"""

import time
import logging

from pyxmas import get_ttn_access_layer, sensors_topic, SensorsTTNPayload
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, TTN_PORT


logging.basicConfig(level=logging.INFO)


def on_sensors_data(sensors_data: SensorsTTNPayload):
    print(sensors_data)


def main():
    with get_ttn_access_layer(
        app_id=TTN_APP_ID,
        api_key=TTN_API_KEY,
        addr=TTN_BASE_URL,
        port=TTN_PORT,
        topic=sensors_topic,
        on_message=on_sensors_data,
    ):
        time.sleep(300)  # Listen for 300 seconds


if __name__ == "__main__":
    main()

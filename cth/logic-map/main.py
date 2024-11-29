"""

    Main script to start the LOGIC MAPPER!

    - Reads the values from the sensors from the UPLINK topic
    - Sends actions accordingly to the DOWNLINK topic



"""

import time
import logging
from typing import List
from ttn_al import get_ttn_access_layer
from topics import sensors_topic, actions_topic, ActionsTTNPayload, SensorsTTNPayload, ActionsEnum
from settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("logic-mapper")


def el_famoso_logic_mapper(sensors_data: SensorsTTNPayload) -> List[ActionsTTNPayload]:
    """
    El famoso logic mapper implementation.
    Takes data from the sensors as inputs and returns one or multiple actions.
    """

    if sensors_data.humidity > 50:
        logger.info(f"Humidity is {sensors_data.humidity}%")
        return [ActionsTTNPayload(action=ActionsEnum.VILLAGE_LED)]

    # some other rules here ...


def on_sensors_data(sensors_data: SensorsTTNPayload):
    actions = el_famoso_logic_mapper(sensors_data)
    if actions:
        with get_ttn_access_layer(
            TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, actions_topic
        ) as ttn:
            for action in actions:
                ttn.publish(action)


def main():
    with get_ttn_access_layer(
        TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, sensors_topic, on_message=on_sensors_data
    ):
        time.sleep(500)  # Listen for 500 seconds


if __name__ == "__main__":
    main()

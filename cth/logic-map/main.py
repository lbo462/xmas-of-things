import time
import logging
from ttn_al import get_ttn_access_layer
from topics import sensors_topic, actions_topic, ActionsTTNPayload, actions_queued_topic
from settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL


logging.basicConfig(level=logging.DEBUG)


def print_message(message):
    print(message)


def main():
    with get_ttn_access_layer(
        TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, actions_topic
    ) as ttn:
        ttn.publish(ActionsTTNPayload(action="coucou"))

    with get_ttn_access_layer(
        TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, actions_queued_topic, on_message=print_message
    ):
        time.sleep(10)


if __name__ == "__main__":
    main()

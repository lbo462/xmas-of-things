import os
import time
import logging
from dotenv import load_dotenv
from ttn_access_layer import get_ttn_access_layer, TTNMessage

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

TTN_APP_ID = os.getenv("TTN_APP_ID")
TTN_API_KEY = os.getenv("TTN_API_KEY")
TTN_BASE_URL = os.getenv("TTN_BASE_URL")
TTN_SENSORS_TOPIC = os.getenv("TTN_SENSORS_TOPIC")


def on_message(message: TTNMessage):
    print(message)


def main():
    with get_ttn_access_layer(
        TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, TTN_SENSORS_TOPIC, on_message=on_message
    ):
        time.sleep(10)


if __name__ == "__main__":
    main()

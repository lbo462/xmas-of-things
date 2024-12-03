"""

    Simple subscription to the DOWNLINK topic and reads actions sent.

"""

import time
import logging

from pyxmas import get_ttn_access_layer, ActionsTTNPayload, actions_queued_topic
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, TTN_PORT


logging.basicConfig(level=logging.INFO)


def on_action_queued(action: ActionsTTNPayload):
    print(action.to_json())


def main():
    with get_ttn_access_layer(
        app_id=TTN_APP_ID,
        api_key=TTN_API_KEY,
        addr=TTN_BASE_URL,
        port=TTN_PORT,
        topic=actions_queued_topic,
        on_message=on_action_queued,
    ):
        time.sleep(300)  # Listen for 300 seconds


if __name__ == "__main__":
    main()

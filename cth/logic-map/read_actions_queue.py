"""

    Simple subscription to the DOWNLINK topic and reads actions sent.

"""

import time
import logging
from ttn_al import get_ttn_access_layer
from topics import ActionsTTNPayload, actions_queued_topic
from settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL


logging.basicConfig(level=logging.INFO)


def on_action_queued(action: ActionsTTNPayload):
    print(action.to_json())


def main():
    with get_ttn_access_layer(
        TTN_APP_ID,
        TTN_API_KEY,
        TTN_BASE_URL,
        actions_queued_topic,
        on_message=on_action_queued,
    ):
        time.sleep(500)  # Listen for 500 seconds


if __name__ == "__main__":
    main()

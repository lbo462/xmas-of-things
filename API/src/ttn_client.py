# API/src/ttn_client.py

import logging
from pyxmas import (
    get_ttn_access_layer,
    ActionsTTNPayload,
    actions_topic,
)
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, TTN_PORT

logger = logging.getLogger(__name__)

def send_downlink(action_payload: ActionsTTNPayload):
    """
    Sends a downlink action to TTN.

    :param action_payload: An instance of ActionsTTNPayload containing the action details.
    """
    try:
        with get_ttn_access_layer(
            app_id=TTN_APP_ID,
            api_key=TTN_API_KEY,
            addr=TTN_BASE_URL,
            port=TTN_PORT,
            topic=actions_topic,
        ) as ttn:
            ttn.publish(action_payload)
            logger.info(f"Sent action: {action_payload.to_json()}")
    except Exception as e:
        logger.error(f"Failed to send downlink: {e}")
        raise e

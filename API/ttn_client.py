import os
import json
import requests
import logging
from settings import TTN_APP_ID, TTN_DEVICE_ID, TTN_API_KEY, TTN_BASE_URL

logger = logging.getLogger(__name__)

def send_downlink(action_id, action_name, parameters=None):
    url = f"https://{TTN_BASE_URL}/api/v3/as/applications/{TTN_APP_ID}/devices/{TTN_DEVICE_ID}/down/push"
    headers = {
        'Authorization': f'Bearer {TTN_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Prepare payload_fields
    payload_fields = {
        "action_id": action_id,
        "action_name": action_name
    }

    if parameters:
        payload_fields.update(parameters)

    payload = {
        "downlinks": [
            {
                "f_port": 1,
                "frm_payload": "",  # Will be filled by TTN's encoder
                "priority": "NORMAL",
                "decoded_payload": payload_fields
            }
        ]
    }

    try:
        logger.debug(f"Sending downlink request to TTN: {json.dumps(payload)}")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info(f"Downlink queued successfully: {json.dumps(payload_fields)}")
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
        logger.error(f"Response content: {response.content.decode('utf-8')}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")

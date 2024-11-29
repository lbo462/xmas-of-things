import os
import json
import base64
import requests
import logging
from settings import TTN_APP_ID, TTN_DEVICE_ID, TTN_API_KEY, TTN_BASE_URL

logger = logging.getLogger(__name__)

def send_downlink(action_id, parameters=None):
    url = f"{TTN_BASE_URL}/api/v3/as/applications/{TTN_APP_ID}/devices/{TTN_DEVICE_ID}/down/push"
    headers = {
        'Authorization': f'Bearer {TTN_API_KEY}',
        'Content-Type': 'application/json'
    }

    bytes_list = [action_id]
    if parameters and 'duration' in parameters:
        duration = parameters['duration']
        bytes_list.append((duration >> 8) & 0xFF)
        bytes_list.append(duration & 0xFF)

    frm_payload = base64.b64encode(bytes(bytes_list)).decode('utf-8')

    payload = {
        "downlinks": [
            {
                "f_port": 1,
                "frm_payload": frm_payload,
                "priority": "NORMAL"
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info(f"Downlink queued successfully: Action ID {action_id}")
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")

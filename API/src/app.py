# API/src/app.py

import os
import threading
import logging
from flask import Flask, render_template, request, jsonify
from pyxmas.logic_map import LogicMap
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, TTN_PORT
from pyxmas.topics import sensors_topic, actions_topic, ActionsEnum, ActionsTTNPayload
from pyxmas.ttn_al.access_layer import TTNAccessLayer  # Import TTNAccessLayer directly
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




app = Flask(__name__)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize VillageState
from pyxmas.state import VillageState
village_state = VillageState()

# Initialize LogicMap without ttn_tenant_id
logic_map = LogicMap(
    ttn_app_id=TTN_APP_ID,
    ttn_api_key=TTN_API_KEY,
    ttn_base_url=TTN_BASE_URL,
    ttn_port=TTN_PORT,
    sensor_topic=sensors_topic,
    action_topic=actions_topic,
    village_state=village_state,
)

def start_logic_map():
    logic_map.start()
    logger.info("LogicMap started.")

# Start LogicMap in a separate daemon thread
logic_thread = threading.Thread(target=start_logic_map)
logic_thread.daemon = True
logic_thread.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    status_message = None
    status_type = None  # 'success' or 'danger'

    if request.method == 'POST':
        action_id = request.form.get('action_id')

        # Validate action_id
        try:
            action_id = int(action_id)
            if action_id not in ActionsEnum._value2member_map_:
                raise ValueError("Invalid action ID.")
            action_enum = ActionsEnum(action_id)
        except (ValueError, TypeError) as e:
            status_message = f"Error: {e}"
            status_type = "danger"
            logger.error(f"Action ID validation error: {e}")
            # Proceed to render the page with the error message
            sensor_data = logic_map.last_sensors_data
            actions = get_available_actions()
            return render_template(
                'index.html',
                sensor_data=sensor_data,
                actions=actions,
                status_message=status_message,
                status_type=status_type
            )

        # Create the action payload without duration
        action_payload = ActionsTTNPayload(action=action_enum)

        # Send the downlink using TTNAccessLayer from ttn_al
        try:
            # Initialize TTNAccessLayer for downlink
            ttn_downlink = TTNAccessLayer(
                app_id=TTN_APP_ID,
                api_key=TTN_API_KEY,
                addr=TTN_BASE_URL,
                topic=actions_topic,
                on_message=None,  # No callback needed for downlinks
                port=TTN_PORT,
            )
            ttn_downlink.start()
            ttn_downlink.publish(action_payload)
            ttn_downlink.stop()

            status_message = f"Action '{action_enum.name}' sent successfully!"
            status_type = "success"
            logger.info(f"Sent action: {action_payload.to_json()}")
        except Exception as e:
            status_message = f"Failed to send action: {e}"
            status_type = "danger"
            logger.error(f"Failed to send action: {e}")

    # Retrieve the latest sensor data from LogicMap
    sensor_data = logic_map.last_sensors_data

    # Prepare actions for the dropdown
    actions = get_available_actions()

    return render_template(
        'index.html',
        sensor_data=sensor_data,
        actions=actions,
        status_message=status_message,
        status_type=status_type
    )

@app.route('/sensor_data', methods=['GET'])
def sensor_data_route():
    """Endpoint to return the latest sensor data as JSON."""
    sensor_data_entry = logic_map.last_sensors_data
    if sensor_data_entry:
        data = {
            "temperature": sensor_data_entry.data.temperature,
            "brightness": sensor_data_entry.data.brightness,
            "loudness": sensor_data_entry.data.loudness,
            "timestamp": sensor_data_entry.datetime_.strftime('%Y-%m-%d %H:%M:%S UTC')
        }
    else:
        data = {
            "temperature": "N/A",
            "brightness": "N/A",
            "loudness": "N/A",
            "timestamp": "N/A"
        }
    return jsonify(data)

def get_available_actions():
    return {action.value: action.name.replace('_', ' ').title() for action in ActionsEnum}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

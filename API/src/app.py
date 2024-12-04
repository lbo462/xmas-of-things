# API/src/app.py

import sys
import os
import threading
import time
import logging
from flask import Flask, render_template, request, jsonify
from pyxmas import (
    get_ttn_access_layer,
    SensorsTTNPayload,
    ActionsTTNPayload,
    ActionsEnum,
    sensors_topic,
    actions_topic,
)
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, TTN_PORT
from datetime import datetime, timezone

# Ensure pyxmas is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyxmas')))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key in production

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the latest sensor data
latest_sensor_data = {
    'brightness': 'N/A',
    'loudness': 'N/A',
    'temperature': 'N/A',
    'timestamp': 'N/A'
}
data_lock = threading.Lock()

def on_sensors_data(sensors_data: SensorsTTNPayload):
    global latest_sensor_data
    with data_lock:
        latest_sensor_data = {
            'brightness': sensors_data.brightness,
            'loudness': sensors_data.loudness,
            'temperature': sensors_data.temperature,
            'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        }
    logger.info(f"Received sensor data: {latest_sensor_data}")

def start_ttn_listener():
    try:
        with get_ttn_access_layer(
            app_id=TTN_APP_ID,
            api_key=TTN_API_KEY,
            addr=TTN_BASE_URL,
            port=TTN_PORT,
            topic=sensors_topic,
            on_message=on_sensors_data,
        ) as ttn:
            logger.info("TTN listener started and listening for sensor data...")
            while True:
                time.sleep(1)
    except Exception as e:
        logger.error(f"TTN listener encountered an error: {e}")

# Start the TTN listener in a separate daemon thread
ttn_thread = threading.Thread(target=start_ttn_listener)
ttn_thread.daemon = True
ttn_thread.start()

# Import send_downlink after setting up the listener to avoid circular imports
from ttn_client import send_downlink

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
            sensor_data = get_latest_sensor_data()
            actions = get_available_actions()
            return render_template('index.html', sensor_data=sensor_data, actions=actions, status_message=status_message, status_type=status_type)

        # Create the action payload without duration
        action_payload = ActionsTTNPayload(action=action_enum)

        # Send the downlink using ttn_client.py
        try:
            send_downlink(action_payload)
            status_message = f"Action '{action_enum.name}' sent successfully!"
            status_type = "success"
        except Exception as e:
            status_message = f"Failed to send action: {e}"
            status_type = "danger"
            logger.error(f"Failed to send action: {e}")

    # Retrieve the latest sensor data
    sensor_data = get_latest_sensor_data()

    # Prepare actions for the dropdown
    actions = get_available_actions()

    return render_template('index.html', sensor_data=sensor_data, actions=actions, status_message=status_message, status_type=status_type)

@app.route('/sensor_data', methods=['GET'])
def sensor_data():
    """Endpoint to return the latest sensor data as JSON."""
    sensor_data = get_latest_sensor_data()
    return jsonify(sensor_data)

def get_latest_sensor_data():
    with data_lock:
        return latest_sensor_data.copy()

def get_available_actions():
    return {action.value: action.name for action in ActionsEnum}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

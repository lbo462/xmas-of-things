from flask import Flask, render_template, request, redirect
from ttn_client import send_downlink
from settings import TTN_APP_ID, TTN_DEVICE_ID, TTN_API_KEY, TTN_BASE_URL
import logging
from ttn_al import get_ttn_access_layer
from topics import sensors_topic, SensorsTTNPayload
import threading
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the latest sensor data
latest_sensor_data = None
data_lock = threading.Lock()

def on_sensors_data(sensors_data: SensorsTTNPayload):
    global latest_sensor_data
    with data_lock:
        latest_sensor_data = {
            'temperature': sensors_data.temperature,
            'humidity': sensors_data.humidity
        }
    logger.info(f"Received sensor data: {latest_sensor_data}")

def start_ttn_listener():
    try:
        with get_ttn_access_layer(
            TTN_APP_ID, TTN_API_KEY, TTN_BASE_URL, sensors_topic, on_message=on_sensors_data
        ):
            while True:
                time.sleep(1)
    except Exception as e:
        logger.error(f"TTN listener encountered an error: {e}")

# Start the TTN listener in a separate thread
ttn_thread = threading.Thread(target=start_ttn_listener)
ttn_thread.daemon = True
ttn_thread.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action_id = int(request.form['action_id'])
        duration = int(request.form.get('duration', 0))
        parameters = {'duration': duration} if duration > 0 else None
        send_downlink(action_id, parameters)
        return redirect('/')
    # Retrieve sensor data
    sensor_data = get_sensor_data()
    return render_template('index.html', sensor_data=sensor_data)

def get_sensor_data():
    with data_lock:
        if latest_sensor_data:
            return latest_sensor_data
        else:
            return {
                'temperature': 'N/A',
                'humidity': 'N/A'
            }

if __name__ == '__main__':
    app.run(debug=True)

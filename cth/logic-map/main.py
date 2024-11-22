import os
from dotenv import load_dotenv
from ttn_access_layer import TTNAccessLayer, TTNMessage

load_dotenv()

TTN_APP_ID = os.getenv('TTN_APP_ID')
TTN_API_KEY = os.getenv('TTN_API_KEY')
TTN_BASE_URL = os.getenv('TTN_BASE_URL')
TTN_SENSORS_TOPIC = os.getenv('TTN_SENSORS_TOPIC')


def on_message(message: TTNMessage):
    print(message)


ttn = TTNAccessLayer(
    TTN_APP_ID,
    TTN_API_KEY,
    TTN_BASE_URL,
    TTN_SENSORS_TOPIC,
    on_message=on_message
)
ttn.loop()

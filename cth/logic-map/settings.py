import os
from dotenv import load_dotenv

load_dotenv()

TTN_APP_ID = os.getenv("TTN_APP_ID")
TTN_API_KEY = os.getenv("TTN_API_KEY")
TTN_BASE_URL = os.getenv("TTN_BASE_URL")
TTN_SENSORS_TOPIC = os.getenv("TTN_SENSORS_TOPIC")
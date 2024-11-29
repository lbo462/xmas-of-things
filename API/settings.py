import os
from dotenv import load_dotenv

load_dotenv()

TTN_APP_ID = os.getenv('TTN_APP_ID')  # 'sensor-downlink'
TTN_TENANT_ID = os.getenv('TTN_TENANT_ID', 'ttn')
TTN_DEVICE_ID = os.getenv('TTN_DEVICE_ID')  # 'testarduino'
TTN_API_KEY = os.getenv('TTN_API_KEY')
TTN_BASE_URL = 'eu1.cloud.thethings.network'

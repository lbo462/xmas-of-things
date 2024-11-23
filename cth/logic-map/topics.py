from ttn_al.topics import TTNBasePayload, Topic
from settings import TTN_SENSORS_TOPIC

class SensorsTTNPayload(TTNBasePayload):
    """Decoded payload for receiving sensors data"""

    humidity: int
    temperature: int

sensors_topic = Topic(uri=TTN_SENSORS_TOPIC, payload_model=SensorsTTNPayload)

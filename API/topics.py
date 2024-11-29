from dataclasses import dataclass
from ttn_al.topics import TTNBasePayload, Topic, TopicTypesEnum
from settings import TTN_APP_ID, TTN_TENANT_ID, TTN_DEVICE_ID

@dataclass
class SensorsTTNPayload(TTNBasePayload):
    """Decoded payload for receiving sensors data"""
    brightness: int
    loudness: int
    temperature: int

sensors_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id=TTN_DEVICE_ID,
    type_=TopicTypesEnum.UP,
    payload_model=SensorsTTNPayload,
)

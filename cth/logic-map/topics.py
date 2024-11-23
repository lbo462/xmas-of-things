from dataclasses import dataclass

from ttn_al.topics import TTNBasePayload, Topic, TopicTypesEnum
from settings import TTN_APP_ID, TTN_TENANT_ID


@dataclass
class SensorsTTNPayload(TTNBasePayload):
    """Decoded payload for receiving sensors data"""

    humidity: int
    temperature: int


@dataclass
class ActionsTTNPayload(TTNBasePayload):
    """Actions payload to send to TTN"""

    action: str


sensors_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="sensor-test",
    type_=TopicTypesEnum.UP,
    payload_model=SensorsTTNPayload
)

actions_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="sensor-test",
    type_=TopicTypesEnum.DOWN_PUSH,
    payload_model=ActionsTTNPayload
)

actions_queued_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="sensor-test",
    type_=TopicTypesEnum.DOWN_QUEUED,
    payload_model=ActionsTTNPayload
)

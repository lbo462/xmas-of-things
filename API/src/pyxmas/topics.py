from dataclasses import dataclass
from typing import Dict

from .ttn_al.topics import TTNBasePayload, Topic, TopicTypesEnum
from .settings import TTN_APP_ID, TTN_TENANT_ID
from .actions import ActionsEnum


@dataclass
class SensorsTTNPayload(TTNBasePayload):
    """Decoded payload for receiving sensors data"""

    temperature: int
    brightness: int


@dataclass
class ActionsTTNPayload(TTNBasePayload):
    """Actions payload to send to TTN"""

    action: ActionsEnum

    @classmethod
    def from_dict(cls, d: Dict) -> "ActionsTTNPayload":
        return cls(action=ActionsEnum(d["action_id"]))

    def to_json(self) -> Dict:
        return {
            "action_id": self.action.value,
            "human_name": self.action.name,
        }


sensors_topic = Topic(  # sensors
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="testarduino",
    type_=TopicTypesEnum.UP,
    payload_model=SensorsTTNPayload,
)

wheel_topic = Topic(  # ferris wheel actionner
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="big-wheel",
    type_=TopicTypesEnum.DOWN_PUSH,
    payload_model=ActionsTTNPayload,
)

leds_topic = Topic(  # leds actionner
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="christmas-star-village-star",
    type_=TopicTypesEnum.DOWN_PUSH,
    payload_model=ActionsTTNPayload,
)

carousel_topic = Topic(  # carousel actionner
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="manege",
    type_=TopicTypesEnum.DOWN_PUSH,
    payload_model=ActionsTTNPayload,
)

lcd_buzzer = Topic(  # lcd/buzzer actionners
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="lcd-receiver",
    type_=TopicTypesEnum.DOWN_PUSH,
    payload_model=ActionsTTNPayload,
)

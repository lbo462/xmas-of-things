from dataclasses import dataclass
from typing import Dict, List

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


def get_actions_per_topic(topic: Topic) -> List[ActionsEnum]:
    if topic is wheel_topic:
        return [ActionsEnum.FERRIS_WHEEL_ON, ActionsEnum.FERRIS_WHEEL_OFF]
    elif topic is leds_topic:
        return [
            ActionsEnum.LEDS_TREE_OFF,
            ActionsEnum.LEDS_TREE_ON,
            ActionsEnum.LEDS_VILLAGE_OFF,
            ActionsEnum.LEDS_VILLAGE_ON,
        ]
    elif topic is carousel_topic:
        return [ActionsEnum.CAROUSEL_OFF, ActionsEnum.CAROUSEL_ON]
    elif topic is lcd_buzzer:
        return [
            ActionsEnum.LCD_1,
            ActionsEnum.LCD_2,
            ActionsEnum.LCD_COLD,
            ActionsEnum.LCD_HOT,
            ActionsEnum.LCD_OFF,
            ActionsEnum.BUZZERS_1,
            ActionsEnum.BUZZERS_2,
            ActionsEnum.BUZZERS_3,
            ActionsEnum.BUZZERS_OFF,
        ]
    else:
        raise NotImplementedError(f"{topic} not handled.")

from dataclasses import dataclass
from typing import Dict
from enum import IntEnum

from ttn_al.topics import TTNBasePayload, Topic, TopicTypesEnum
from settings import TTN_APP_ID, TTN_TENANT_ID


class ActionsEnum(IntEnum):
    """
    Defines every possible actions in the village.
    The enum value correspond to the value read by the CTH to activate its things.
    """

    XMAS_TREE_LED = 0
    XMAS_TREE_STAR = 1
    VILLAGE_LED = 2
    SANTA_TRACK_LED = 3
    SNOW_SPRAY = 4


@dataclass
class SensorsTTNPayload(TTNBasePayload):
    """Decoded payload for receiving sensors data"""

    humidity: int
    temperature: int


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


sensors_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="sensor-test",
    type_=TopicTypesEnum.UP,
    payload_model=SensorsTTNPayload,
)

actions_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="sensor-test",
    type_=TopicTypesEnum.DOWN_PUSH,
    payload_model=ActionsTTNPayload,
)

actions_queued_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="sensor-test",
    type_=TopicTypesEnum.DOWN_QUEUED,
    payload_model=ActionsTTNPayload,
)

from dataclasses import dataclass
from typing import Dict
from enum import IntEnum

from .ttn_al.topics import TTNBasePayload, Topic, TopicTypesEnum
from .settings import TTN_APP_ID, TTN_TENANT_ID


class ActionsEnum(IntEnum):
    """
    Defines every possible actions in the village.
    The enum value correspond to the value read by the CTH to activate its things.
    """
    #### MARY_GO_ON ####
    MARY_GO_ON_ON = 0
    MARY_GO_ON_OFF = 1
    #### FERRIS_WHEEL ####
    FERRIS_WHEEL_ON = 10
    FERRIS_WHEEL_OFF = 11
    #### BUZZERS ####
    BUZZERS_1 = 20
    BUZZERS_2 = 21
    BUZZERS_3 = 22
    BUZZERS_OFF = 23
    #### LEDS ####
    LEDS_TREE_ON = 30
    LEDS_TREE_OFF = 31
    LEDS_VILLAGE_ON = 32
    LEDS_VILLAGE_OFF = 33
    #### LCD ####
    LCD_1 = 40
    LCD_2 = 41
    LCD_OFF = 42

"""     #### LEDS ####

    XMAS_TREE_LED = 0
    XMAS_TREE_STAR = 1
    VILLAGE_LED = 2
    SANTA_TRACK_LED = 3

    #### SPRAY ####

    SNOW_SPRAY = 4

    #### SONGS ####
    STOP_MUSIC = 10
    PLAY_SONG_1 = 11
    PLAY_SONG_2 = 12
    PLAY_SONG_3 = 13

    #### MESSAGES ####

    DISPLAY_NO_MESSAGE = 20
    DISPLAY_MESSAGE_1 = 21
    DISPLAY_MESSAGE_2 = 22

    #### GRANDE ROUE ####

    START_WHEEL = 30 """


@dataclass
class SensorsTTNPayload(TTNBasePayload):
    """Decoded payload for receiving sensors data"""

    temperature: int
    brightness: int
    loudness: int


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

actions_topic = Topic(  # actionners
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="cth-device",
    type_=TopicTypesEnum.DOWN_PUSH,
    payload_model=ActionsTTNPayload,
)

actions_queued_topic = Topic(  # monitoring
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id="cth-device",
    type_=TopicTypesEnum.DOWN_QUEUED,
    payload_model=ActionsTTNPayload,
)

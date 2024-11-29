from dataclasses import dataclass
from typing import Dict
from enum import IntEnum
from ttn_al.topics import TTNBasePayload, Topic, TopicTypesEnum
from settings import TTN_APP_ID, TTN_TENANT_ID, TTN_DEVICE_ID

class ActionsEnum(IntEnum):
    """
    Defines every possible action in the village.
    """
    XMAS_TREE_LED = 1
    XMAS_TREE_STAR = 2
    VILLAGE_LED = 3
    SANTA_TRACK_LED = 4
    SNOW_SPRAY = 5

@dataclass
class SensorsTTNPayload(TTNBasePayload):
    """Decoded payload for receiving sensors data"""
    humidity: int
    temperature: int

sensors_topic = Topic(
    app_id=TTN_APP_ID,
    tenant_id=TTN_TENANT_ID,
    device_id=TTN_DEVICE_ID,
    type_=TopicTypesEnum.UP,
    payload_model=SensorsTTNPayload,
)

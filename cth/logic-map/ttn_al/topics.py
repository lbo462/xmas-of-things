import json
from typing import TypeVar, Type, Dict, Callable
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum


@dataclass_json
@dataclass
class TTNBasePayload:
    """Template for TTN payloads"""


T = TypeVar("T", bound=TTNBasePayload)


def uplink_topic_extractor(payload: str | bytes | bytearray) -> Dict:
    decoded_payload = json.loads(payload)
    return decoded_payload["uplink_message"]["decoded_payload"]


def downlink_topic_extractor(payload: str | bytes | bytearray) -> Dict:
    decoded_payload = json.loads(payload)
    return decoded_payload["downlink_queued"]["decoded_payload"]


class TopicTypesEnum(Enum):
    """All the different types of topics"""

    UP = "up"
    DOWN_PUSH = "down/push"
    DOWN_QUEUED = "down/queued"

    @property
    def payload_extractor(self) -> Callable[[str | bytes | bytearray], Dict] | None:
        return {
            "UP": uplink_topic_extractor,
            "DOWN_PUSH": None,  # topic is "write only"
            "DOWN_QUEUED": downlink_topic_extractor,
        }[self.name]


@dataclass
class Topic:
    """TTN topic"""

    app_id: str
    tenant_id: str
    device_id: str

    type_: TopicTypesEnum
    """Type of the topic: UP / DOWN / ..."""

    payload_model: Type[T] | None
    """Expected model response from TTN OR payload to send in case of a downlink topic"""

    @property
    def uri(self) -> str:
        return f"v3/{self.app_id}@{self.tenant_id}/devices/{self.device_id}/{self.type_.value}"

    @property
    def payload_extractor(self) -> Callable[[str | bytes | bytearray], Dict] | None:
        return self.type_.payload_extractor

    def __str__(self):
        return f"{self.uri} {self.payload_model.__name__}"

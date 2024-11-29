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

def uplink_topic_extractor(payload: bytes) -> Dict:
    decoded_payload = json.loads(payload.decode('utf-8'))
    return decoded_payload["uplink_message"]["decoded_payload"]

class TopicTypesEnum(Enum):
    """All the different types of topics"""
    UP = "up"
    DOWN_PUSH = "down/push"
    DOWN_QUEUED = "down/queued"

    @property
    def payload_extractor(self) -> Callable[[bytes], Dict]:
        return {
            "UP": uplink_topic_extractor,
            "DOWN_PUSH": None,  # Topic is "write only"
            "DOWN_QUEUED": None,  # Implement if needed
        }[self.name]

@dataclass
class Topic:
    """TTN topic"""
    app_id: str
    tenant_id: str
    device_id: str
    type_: TopicTypesEnum
    payload_model: Type[T]

    @property
    def uri(self) -> str:
        return f"v3/{self.app_id}@{self.tenant_id}/devices/{self.device_id}/{self.type_.value}"

    @property
    def payload_extractor(self) -> Callable[[bytes], Dict]:
        return self.type_.payload_extractor

    def __str__(self):
        return f"{self.uri} {self.payload_model.__name__}"

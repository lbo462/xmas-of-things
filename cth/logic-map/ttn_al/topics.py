from typing import TypeVar
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TTNBasePayload:
    """Template for TTN payloads"""

T = TypeVar('T', bound=TTNBasePayload)

@dataclass
class Topic:
    """TTN topic"""

    uri: str
    """URI of the topic. Example: v3/{application id}@{tenant id}/devices/{device id}/down/push"""

    payload_model: T
    """Expected model response from TTN"""

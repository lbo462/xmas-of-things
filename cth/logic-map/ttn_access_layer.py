import json
import paho.mqtt.client as mqtt
from typing import Callable
from dataclasses import dataclass
from dataclasses_json import dataclass_json



@dataclass_json
@dataclass
class TTNMessage:
    """
    Payload content retrieved from TTN
    """

    humidity: int
    temperature: int


class TTNAccessLayer:
    """
    TTN access layer handling the connection to TTN together with some payload decoder functions.
    """


    def __init__(
        self, app_id: str, api_key: str, addr: str, topic, on_message: Callable[[TTNMessage], None], port: int = 1883
    ):
        """
        Creates an access layer.
        :param app_id: Of the form "app_name@ttn"
        :param api_key: API key for the given TTN app
        :param addr: Base URL for accessing TTN
        :param topic: Channel to which this access layer subscribes
        """
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._client.on_connect = self._get_on_connect(topic)
        self._client.on_message = self._get_on_message(on_message)

        self._client.username_pw_set(app_id, api_key)
        self._client.connect(addr, port)

    def _get_on_connect(self, topic: str):
        """Create the on_connect function for the mqtt client"""

        def on_connect(client, userdata, flags, reason_code, properties):
            client.subscribe(topic)

        return on_connect

    def _get_on_message(self, on_message_callback: Callable[[TTNMessage], None]):
        """Create the on_message function for the mqtt client"""

        def on_message(client, userdata, msg):
            payload = json.loads(msg.payload)
            decoded_payload = payload["uplink_message"]["decoded_payload"]
            on_message_callback(TTNMessage.from_dict(decoded_payload))

        return on_message

    def loop(self):
        """Start listening forever and ever!"""
        self._client.loop_forever()

    def __str__(self) -> str:
        return f"Client to {self._topic}"


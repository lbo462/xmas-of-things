import json
import logging
import paho.mqtt.client as mqtt
from typing import Callable, ContextManager
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from contextlib import contextmanager


logger = logging.getLogger(__name__)


@dataclass_json
@dataclass
class TTNMessage:
    """
    Payload content retrieved from TTN
    """

    humidity: int
    temperature: int


class _TTNAccessLayer:
    """
    TTN access layer handling the connection to TTN together with some payload decoder functions.
    Do not call directly, use the context manager instead.
    """

    def __init__(
        self,
        app_id: str,
        api_key: str,
        addr: str,
        topic,
        on_message: Callable[[TTNMessage], None] | None = None,
        port: int = 1883,
    ):
        """
        Creates an access layer to TTN
        :param app_id: Of the form "app_name@ttn"
        :param api_key: API key for the given TTN app
        :param addr: Base URL for accessing TTN
        :param topic: Channel to which this access layer subscribes
        :param on_message: Callback function to trigger when a message is received
        """
        self._topic = topic
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._client.on_connect = self._get_on_connect(topic)
        self._client.on_message = self._get_on_message(on_message)

        self._client.username_pw_set(app_id, api_key)
        self._client.connect(addr, port)
        logger.debug(f"{self} connected successfully to TTN")

    def _get_on_connect(self, topic: str):
        """Create the on_connect function for the mqtt client"""

        def on_connect(client, userdata, flags, reason_code, properties):
            client.subscribe(topic)
            logger.debug(f"{self} subscribed")

        return on_connect

    def _get_on_message(
        self, on_message_callback: Callable[[TTNMessage], None] | None = None
    ):
        """Create the on_message function for the mqtt client"""

        def on_message(client, userdata, msg):
            logger.debug(
                f"Message received on {self} (payload length: {len(msg.payload)})"
            )

            if on_message_callback:
                payload = json.loads(msg.payload)
                decoded_payload = payload["uplink_message"]["decoded_payload"]
                ttn_message = TTNMessage.from_dict(decoded_payload)
                logger.debug(
                    f"Payload decoded, triggering callback function with {ttn_message}"
                )
                on_message_callback(ttn_message)

            else:
                logger.debug(f"No callback function to call, continuing ...")

        return on_message

    def start(self):
        """Start listening channel"""
        self._client.loop_start()
        logger.info(f"{self} started listening")

    def stop(self):
        """Stop listening"""
        self._client.loop_stop()
        logger.info(f"{self} stopped listening")

    def __str__(self) -> str:
        return f"Client to {self._topic}"


@contextmanager
def get_ttn_access_layer(
    app_id: str,
    api_key: str,
    addr: str,
    topic,
    on_message: Callable[[TTNMessage], None],
    port: int = 1883,
) -> ContextManager[_TTNAccessLayer]:
    """
    Creates an access layer to TTN
    :param app_id: Of the form "app_name@ttn"
    :param api_key: API key for the given TTN app
    :param addr: Base URL for accessing TTN
    :param topic: Channel to which this access layer subscribes
    :param on_message: Callback function to trigger when a message is received
    """
    ttn = _TTNAccessLayer(
        app_id=app_id,
        api_key=api_key,
        addr=addr,
        topic=topic,
        on_message=on_message,
        port=port,
    )
    ttn.start()
    yield ttn
    ttn.stop()

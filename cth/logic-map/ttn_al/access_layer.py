import json
import logging
import paho.mqtt.client as mqtt
from typing import Callable, ContextManager, TypeVar
from contextlib import contextmanager

from .topics import Topic, TTNBasePayload


logger = logging.getLogger("ttn_access_layer")

T = TypeVar('T', bound=TTNBasePayload)


class TTNAccessLayer:
    """
    TTN access layer handling the connection to TTN together with some payload decoder functions.
    Do not call directly, use the context manager instead.
    """

    def __init__(
        self,
        app_id: str,
        api_key: str,
        addr: str,
        topic: Topic,
        on_message: Callable[[T], None] | None = None,
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
        self._client.enable_logger(logging.getLogger("mqttc"))

        self._client.on_connect = self._get_on_connect()
        self._client.on_message = self._get_on_message(on_message)

        self._client.username_pw_set(app_id, api_key)
        self._client.connect(addr, port)
        logger.debug(f"{self} connected successfully to TTN")

    def _get_on_connect(self):
        """Create the on_connect function for the mqtt client"""

        def on_connect(client, userdata, flags, reason_code, properties):
            client.subscribe(self._topic.uri)
            logger.debug(f"{self} subscribed")

        return on_connect

    def _get_on_message(
        self, on_message_callback: Callable[[T], None] | None = None
    ):
        """Create the on_message function for the mqtt client"""

        def on_message(client, userdata, msg):
            logger.debug(
                f"Message received on {self} (payload length: {len(msg.payload)})"
            )

            if on_message_callback:
                payload = json.loads(msg.payload)
                decoded_payload = payload["uplink_message"]["decoded_payload"]
                ttn_message = self._topic.payload_model.from_dict(decoded_payload)
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
    topic: Topic,
    on_message: Callable[[T], None],
    port: int = 1883,
) -> ContextManager[TTNAccessLayer]:
    """
    Creates an access layer to TTN
    :param app_id: Of the form "app_name@ttn"
    :param api_key: API key for the given TTN app
    :param addr: Base URL for accessing TTN
    :param topic: Channel to which this access layer subscribes
    :param on_message: Callback function to trigger when a message is received
    """
    ttn = TTNAccessLayer(
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

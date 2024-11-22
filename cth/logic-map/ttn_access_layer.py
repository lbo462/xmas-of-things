from typing import Callable
import paho.mqtt.client as mqtt



class TTNAccessLayer:

    def __init__(
        self, username: str, password: str, addr: str, topic, on_message: Callable[[int], None] , port: int = 1883
    ):
        self._topic = topic

        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._client.on_connect = self._get_on_connect()
        self._client.on_message = self._get_on_message(on_message)

        self._client.username_pw_set(username, password)
        self._client.connect(addr, port)

    def _get_on_connect(self):

        def on_connect(client, userdata, flags, reason_code, properties):
            client.subscribe(self._topic)
            print(f"{self} connected.")

        return on_connect

    def _get_on_message(self, callback_on_message: Callable[[int], None]):

        def on_message(client, userdata, msg):
            callback_on_message(msg)

        return on_message

    def loop(self):
        self._client.loop_forever()

    def __str__(self) -> str:
        return f"Client to {self._topic}"


ttn = TTNAccessLayer(
    "username@ttn",
    "api-key",
    "eu1.cloud.thethings.network",
    "v3/username@ttn/devices/<device>/up",
)
ttn.loop()

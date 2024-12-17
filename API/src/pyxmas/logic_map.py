from datetime import datetime
import logging
from typing import List
from dataclasses import dataclass

from .state import VillageState, update_state
from .topics import (
    Topic,
    SensorsTTNPayload,
    ActionsTTNPayload,
    ActionsEnum,
    get_actions_per_topic,
)
from .ttn_al import get_ttn_access_layer
from .ttn_al.access_layer import TTNAccessLayer


@dataclass
class SensorHistoryEntry:
    """
    Defined how an entry is designed in the sensors data history of the logic map.
    """

    data: SensorsTTNPayload
    datetime_: datetime

    def __str__(self):
        return f"{self.datetime_}: {self.data}"


class LogicMap:
    """
    Brain implementation over the TTN access layer.

    Require to be started with `logic_map.start()`.
    Should be stopped with `logic_map.stop()`.

    Two available modes:
    - inactive: Just listen to receive data and stores it into its `sensors_history`
    - active: Same as inactive, but react in real time with data, sends actions defined by `_map()` and update the state.
    """

    def __init__(
        self,
        ttn_app_id: str,
        ttn_api_key: str,
        ttn_base_url: str,
        ttn_port: int,
        sensor_topic: Topic,
        actions_topic: List[Topic],
        village_state: VillageState,
    ):
        self._publish_enabled = False
        self._ttn_app_id = ttn_app_id
        self._ttn_api_key = ttn_api_key
        self._ttn_base_url = ttn_base_url
        self._ttn_port = ttn_port
        self._sensor_topic = sensor_topic
        self._actions_topic = actions_topic
        self._state = village_state

        self._logger = logging.getLogger(__name__)
        self._sensors_history: List[SensorHistoryEntry] = []
        self._ttn_al_sensors = TTNAccessLayer(
            app_id=self._ttn_app_id,
            api_key=self._ttn_api_key,
            addr=self._ttn_base_url,
            port=self._ttn_port,
            topic=self._sensor_topic,
            on_message=self._on_sensors_data,
        )

    @property
    def is_active(self):
        return self._publish_enabled

    def activate(self):
        """Make the logic map react to data. Will send actions and update the village state"""
        self._logger.info("Activated")
        self._publish_enabled = True

    def deactivate(self):
        """Stops the logic map to trigger any action. Passively listen and store data to its history"""
        self._logger.info("Deactivated")
        self._publish_enabled = False

    @property
    def sensors_history(self) -> List[SensorHistoryEntry]:
        """History of every sensor data received, timestamped"""
        return self._sensors_history

    @property
    def last_sensors_data(self) -> SensorHistoryEntry | None:
        """Get the last data received from the sensors, if any data was received"""
        if len(self.sensors_history) > 0:
            return self.sensors_history[-1]
        return None

    def _map(self, sensors_data: SensorsTTNPayload) -> List[ActionsTTNPayload]:
        """
        Heart of the machine.
        Defines, when activated, what actions to take as a function of the current data received.

        :param sensors_data: Data received from the sensors.
        :return: The list of actions to send to the engines.
        """

        actions = []

        # Brightness
        if sensors_data.brightness < 200:
            self._logger.info(f"Brightness is {sensors_data.brightness} lumens.")
            if self._state.leds_tree_on:
                actions.append(ActionsTTNPayload(action=ActionsEnum.LEDS_TREE_OFF))
            if self._state.leds_village_on:
                actions.append(ActionsTTNPayload(action=ActionsEnum.LEDS_VILLAGE_OFF))
        else:
            self._logger.info(f"Brightness is {sensors_data.brightness} lumens.")
            if not self._state.leds_tree_on:
                actions.append(ActionsTTNPayload(action=ActionsEnum.LEDS_TREE_ON))
            if not self._state.leds_village_on:
                actions.append(ActionsTTNPayload(action=ActionsEnum.LEDS_VILLAGE_ON))

        # Temperature
        if sensors_data.temperature >= 25:
            actions.append(ActionsTTNPayload(action=ActionsEnum.LCD_HOT))
        elif sensors_data.temperature <= 20:
            actions.append(ActionsTTNPayload(ActionsEnum.LCD_COLD))

        return actions

    def _on_sensors_data(self, sensors_data: SensorsTTNPayload):
        """
        Callback func passed to the TTN access layer, triggered when a data is received from sensors.
        Logs data to the history, and trigger actions if the logic map is activated.
        """
        self._logger.info(f"Received {sensors_data}")
        self._sensors_history.append(
            SensorHistoryEntry(data=sensors_data, datetime_=datetime.now())
        )

        if self._publish_enabled:
            actions = self._map(sensors_data)
            if actions:
                self.publish_actions(actions)

    def publish_actions(self, actions: List[ActionsTTNPayload]):
        """
        Publish actions on every action topic.
        Actions should not interfere as they have different IDs.
        """
        for topic in self._actions_topic:
            available_actions = get_actions_per_topic(topic)

            with get_ttn_access_layer(
                self._ttn_app_id,
                self._ttn_api_key,
                self._ttn_base_url,
                port=self._ttn_port,
                topic=topic,
            ) as ttn:
                for action in actions:
                    if action.action in available_actions:
                        update_state(action.action, self._state)
                        ttn.publish(action)

    def start(self):
        """Start the logic map, but do not activate it (i.e. only listens, but trigger no actions)"""
        self._ttn_al_sensors.start()

    def stop(self):
        """Stop and deactivate the logic map."""
        if self.is_active:
            self.deactivate()
        self._ttn_al_sensors.stop()

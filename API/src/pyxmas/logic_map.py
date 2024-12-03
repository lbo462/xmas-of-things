import time
from datetime import datetime, UTC
import logging
from typing import List
from dataclasses import dataclass

from .state import VillageState
from .topics import Topic, SensorsTTNPayload, ActionsTTNPayload, ActionsEnum
from .ttn_al import get_ttn_access_layer


@dataclass
class SensorHistoryEntry:
    data: SensorsTTNPayload
    datetime_: datetime

    def __str__(self):
        return f"{self.datetime_}: {self.data}"


class LogicMap:

    def __init__(
        self,
        ttn_app_id: str,
        ttn_api_key: str,
        ttn_base_url: str,
        ttn_port: int,
        sensor_topic: Topic,
        action_topic: Topic,
        village_state: VillageState,
    ):
        self._ttn_app_id = ttn_app_id
        self._ttn_api_key = ttn_api_key
        self._ttn_base_url = ttn_base_url
        self._ttn_port = ttn_port
        self._sensor_topic = sensor_topic
        self._action_topic = action_topic
        self._state = village_state

        self._logger = logging.getLogger(__name__)
        self._sensors_history: List[SensorHistoryEntry] = []

    @property
    def sensors_history(self) -> List[SensorHistoryEntry]:
        """History of every sensor data received, timestamped"""
        return self._sensors_history

    def _map(self, sensors_data: SensorsTTNPayload) -> List[ActionsTTNPayload]:
        actions = []

        if (
            sensors_data.brightness < 100 and self._state.tree_star_on == False
        ):  ##don't forget -- potentially add santa's proximity as condition
            self._logger.info(f"Brightness is {sensors_data.brightness} lumens.")
            actions.append(ActionsTTNPayload(action=ActionsEnum.XMAS_TREE_STAR))
            actions.append(ActionsTTNPayload(action=ActionsEnum.XMAS_TREE_LED))
            self._state.tree_star_on = True
            self._state.tree_led_on = True

        if (
            sensors_data.brightness > 100 and self._state.tree_star_on == True
        ):  ##don't forget -- potentially add santa's proximity as condition
            self._logger.info(f"Brightness is {sensors_data.brightness} lumens.")
            actions.append(ActionsTTNPayload(action=ActionsEnum.XMAS_TREE_STAR))
            actions.append(ActionsTTNPayload(action=ActionsEnum.XMAS_TREE_LED))
            self._state.tree_star_on = False
            self._state.tree_led_on = False

        if sensors_data.loudness > 10 and self._state.village_leds_on == False:
            self._logger.info(f"Loudness is {sensors_data.loudness} dB.")
            actions.append(ActionsTTNPayload(action=ActionsEnum.VILLAGE_LED))
            self._state.village_leds_on = True

        if sensors_data.loudness < 10 and self._state.village_leds_on == True:
            self._logger.info(f"Loudness is {sensors_data.loudness} dB.")
            actions.append(ActionsTTNPayload(action=ActionsEnum.VILLAGE_LED))
            self._state.village_leds_on = False

        if sensors_data.temperature < 30 and self._state.snow_spray == False:
            self._logger.info(f"Temperature is {sensors_data.temperature} C.")
            actions.append(ActionsTTNPayload(action=ActionsEnum.SNOW_SPRAY))
            self._state.snow_spray = True

        if sensors_data.temperature > 30 and self._state.snow_spray == True:
            self._logger.info(f"Temperature is {sensors_data.temperature} C.")
            actions.append(ActionsTTNPayload(action=ActionsEnum.SNOW_SPRAY))
            self._state.snow_spray = False

        return actions

    def _on_sensors_data(self, sensors_data: SensorsTTNPayload):
        self._sensors_history.append(
            SensorHistoryEntry(data=sensors_data, datetime_=datetime.now(UTC))
        )
        actions = self._map(sensors_data)
        if actions:
            self.publish_actions(actions)

    def publish_actions(self, actions: List[ActionsTTNPayload]):
        with get_ttn_access_layer(
            self._ttn_app_id,
            self._ttn_api_key,
            self._ttn_base_url,
            port=self._ttn_port,
            topic=self._action_topic,
        ) as ttn:
            for action in actions:
                ttn.publish(action)

    def start(self, duration: int):
        with get_ttn_access_layer(
            self._ttn_app_id,
            self._ttn_api_key,
            self._ttn_base_url,
            port=self._ttn_port,
            topic=self._sensor_topic,
            on_message=self._on_sensors_data,
        ):
            time.sleep(duration)

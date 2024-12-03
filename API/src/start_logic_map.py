import logging
from time import sleep

from pyxmas import VillageState, LogicMap, sensors_topic, actions_topic
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_PORT, TTN_BASE_URL

logging.basicConfig(level=logging.INFO)

DURATION = 30


def main():
    village_state = VillageState()

    logic_map = LogicMap(
        ttn_app_id=TTN_APP_ID,
        ttn_api_key=TTN_API_KEY,
        ttn_base_url=TTN_BASE_URL,
        ttn_port=TTN_PORT,
        sensor_topic=sensors_topic,
        action_topic=actions_topic,
        village_state=village_state,
    )

    logic_map.start()

    for i in range(0, DURATION):
        # print(f"Last data: {logic_map.last_sensors_data}")  # Constantly print last data received
        sleep(1)

    logic_map.stop()

    for e in logic_map.sensors_history:  # Yay, sensors history!
        print(e)


if __name__ == "__main__":
    main()

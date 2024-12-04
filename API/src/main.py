import logging
from flask import Flask, render_template, jsonify

from pyxmas import VillageState, LogicMap, sensors_topic, actions_topic, ActionsEnum, ActionsTTNPayload
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_PORT, TTN_BASE_URL

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

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


@app.route("/", methods=['GET'])
def index():
    return render_template(
        "index.html",
        actions={action.value: action.name for action in ActionsEnum},
    )


@app.route("/last_sensors_entry", methods=['GET'])
def latest_sensors_entry():
    return jsonify(logic_map.last_sensors_data)


@app.route("/village_state", methods=['GET'])
def get_village_state():
    return jsonify(village_state)


@app.route("/perform_action/<action_id>", methods=['POST'])
def perform_action(action_id: int):
    logic_map.publish_actions([ActionsTTNPayload(ActionsEnum(int(action_id)))])
    return "", 204  # No content


def main():
    """Start Flask app"""

    logic_map.start()

    try:
        app.run()
    finally:
        logic_map.stop()


if __name__ == "__main__":
    main()

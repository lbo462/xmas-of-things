import logging
from flask import Flask, render_template, jsonify, request
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models.sources import AjaxDataSource

from pyxmas import (
    VillageState,
    LogicMap,
    sensors_topic,
    wheel_topic,
    leds_topic,
    carousel_topic,
    lcd_buzzer,
    ActionsEnum,
    ActionsTTNPayload,
)
from pyxmas.settings import TTN_APP_ID, TTN_API_KEY, TTN_PORT, TTN_BASE_URL

logging.basicConfig(level=logging.INFO)

FIGURE_WIDTH = 800
FIGURE_HEIGHT = 300

app = Flask(__name__)

village_state = VillageState()

logic_map = LogicMap(
    ttn_app_id=TTN_APP_ID,
    ttn_api_key=TTN_API_KEY,
    ttn_base_url=TTN_BASE_URL,
    ttn_port=TTN_PORT,
    sensor_topic=sensors_topic,
    actions_topic=[wheel_topic, leds_topic, carousel_topic, lcd_buzzer],
    village_state=village_state,
)


@app.route("/", methods=["GET"])
def index():
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    temperature_source = AjaxDataSource(
        data_url=request.url_root + "/update_temperature",
        polling_interval=1000,
        mode="replace",
    )
    brightness_source = AjaxDataSource(
        data_url=request.url_root + "/update_brightness",
        polling_interval=1000,
        mode="replace",
    )

    fig_temperature = figure(
        width=FIGURE_WIDTH, height=FIGURE_HEIGHT, x_axis_type="datetime"
    )
    fig_brightness = figure(
        width=FIGURE_WIDTH, height=FIGURE_HEIGHT, x_axis_type="datetime"
    )

    fig_temperature.background_fill_alpha = 0
    fig_brightness.background_fill_alpha = 0

    fig_temperature.border_fill_color = "#80ad71"
    fig_brightness.border_fill_color = "#80ad71"

    fig_temperature.line(
        "x",
        "y",
        source=temperature_source,
        legend_label="Temperature",
        line_width=2,
        color="red",
    )
    fig_brightness.line(
        "x",
        "y",
        source=brightness_source,
        legend_label="Brightness",
        line_width=2,
        color="blue",
    )

    script_temperature, div_temperature = components(fig_temperature)
    script_brightness, div_brightness = components(fig_brightness)

    return render_template(
        "index.html",
        actions={action.value: action.name for action in ActionsEnum},
        script_temperature=script_temperature,
        div_temperature=div_temperature,
        script_brightness=script_brightness,
        div_brightness=div_brightness,
        js_resources=js_resources,
        css_resources=css_resources,
    )


@app.route("/update_temperature", methods=["POST"])
def update_temperature():
    temperature_data = [e.data.temperature for e in logic_map.sensors_history]
    datetimes = [e.datetime_.timestamp() for e in logic_map.sensors_history]

    return jsonify(x=datetimes, y=temperature_data)


@app.route("/update_brightness", methods=["POST"])
def update_brightness():
    brightness_data = [e.data.brightness for e in logic_map.sensors_history]
    datetimes = [e.datetime_.timestamp() for e in logic_map.sensors_history]

    return jsonify(x=datetimes, y=brightness_data)


@app.route("/last_sensors_entry", methods=["GET"])
def latest_sensors_entry():
    return jsonify(logic_map.last_sensors_data)


@app.route("/village_state", methods=["GET"])
def get_village_state():
    return jsonify(village_state)


@app.route("/perform_action/<action_id>", methods=["POST"])
def perform_action(action_id: int):
    logic_map.publish_actions([ActionsTTNPayload(ActionsEnum(int(action_id)))])
    return "", 204  # No content


# New route to toggle publishing actions
@app.route("/toggle_publish", methods=["POST"])
def toggle_publish():
    if logic_map.is_active:
        logic_map.deactivate()
    else:
        logic_map.activate()
    return {"publish_enabled": logic_map.is_active}, 200


@app.route("/publish_status", methods=["GET"])
def publish_status():
    return {"publish_enabled": logic_map.is_active}, 200


def main():
    """Start Flask app"""

    logic_map.start()

    try:
        app.run(host="0.0.0.0")
    finally:
        logic_map.stop()


if __name__ == "__main__":
    main()

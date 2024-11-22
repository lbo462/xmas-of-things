import json
import datetime
import paho.mqtt.client as mqtt


DEVICES

APP_ID="sensor-downlink@ttn"
ACCESS_KEY = "NNSXS.HTPOIGZA2Q6TSEOUESE5VABHALWKTHDMTYLW3TA.CATEX5UKOFMQG5HVZSG3P3VY3WORZVQ32R56BXJMY7TK4A5VIPXA"

TOPIC = f"v3/{APP_ID}/devices/sensor-test/up"
print(TOPIC)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):

    
    p = json.loads(msg.payload)
    
    humidity = p["uplink_message"]["decoded_payload"]["humidity"]

    print(humidity)
    

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set(APP_ID, ACCESS_KEY)

mqttc.connect("eu1.cloud.thethings.network", 1883)

mqttc.loop_forever()
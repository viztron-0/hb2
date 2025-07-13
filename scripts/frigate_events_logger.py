# frigate_events_logger.py
import paho.mqtt.client as mqtt, json

BROKER = "127.0.0.1"
USER = "mqtt_user"
PASS = "password"
TOPIC = "frigate/events"

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    if payload["type"] == "new":
        label = payload.get("after", {}).get("label", "unknown")
        print(f"[🚨 DETECTED] {label.upper()} on camera {payload.get('after', {}).get('camera')}")

client = mqtt.Client()
client.username_pw_set(USER, PASS)
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC, qos=1)

print(f"📡 Listening for Frigate events on '{TOPIC}'...")
client.loop_forever()


# drone_dummy.py
#!/usr/bin/env python3
import paho.mqtt.client as mqtt, json

PREFIX, DEVICE_ID, DEVICE_NAME = "homeassistant", "drone_1", "Drone 1"
BROKER, USER, PASS = "127.0.0.1", "mqtt_user", "password"
CMD_TOPIC, STATE_TOPIC = f"homebase/{DEVICE_ID}/cmd", f"homebase/{DEVICE_ID}/status"
DISCOVERY_SENSOR = f"{PREFIX}/sensor/{DEVICE_ID}_action/config"
DISCOVERY_SWITCH = f"{PREFIX}/switch/{DEVICE_ID}_deploy/config"

sensor_payload = {
  "name": f"{DEVICE_NAME} Action",
  "state_topic": STATE_TOPIC,
  "value_template": "{{ value_json.action }}",
  "unique_id": f"{DEVICE_ID}_action",
  "device": {"identifiers":["homebase"],"name":"Homebase System","model":"Dummy Drone","manufacturer":"Viztron"}
}
switch_payload = {
  "name": f"{DEVICE_NAME} Deploy",
  "command_topic": CMD_TOPIC,
  "payload_on": json.dumps({"action":"deploy"}),
  "payload_off": json.dumps({"action":"stop"}),
  "unique_id": f"{DEVICE_ID}_deploy",
  "device": {"identifiers":["homebase"],"name":"Homebase System","model":"Dummy Drone","manufacturer":"Viztron"}
}

def on_message(cli, _, msg):
    print("DRONE CMD:", msg.payload.decode())
    action = json.loads(msg.payload).get("action","unknown")
    cli.publish(STATE_TOPIC, json.dumps({"action":action}), qos=1)

cli = mqtt.Client()
cli.username_pw_set(USER, PASS)
cli.connect(BROKER, 1883, 60)

cli.publish(DISCOVERY_SENSOR, json.dumps(sensor_payload), retain=True)
cli.publish(DISCOVERY_SWITCH, json.dumps(switch_payload), retain=True)
cli.subscribe(CMD_TOPIC, qos=1)
cli.on_message = on_message

print(f"🔄  drone_dummy listening on {CMD_TOPIC}")
cli.loop_forever()


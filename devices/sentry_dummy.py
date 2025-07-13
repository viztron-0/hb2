# sentry_dummy.py
#!/usr/bin/env python3
import paho.mqtt.client as mqtt, json

PREFIX, DEVICE_ID, DEVICE_NAME = "homeassistant", "sentry_1", "Sentry 1"
BROKER, USER, PASS = "127.0.0.1", "mqtt_user", "password"
CMD_TOPIC, STATE_TOPIC = f"homebase/{DEVICE_ID}/cmd", f"homebase/{DEVICE_ID}/status"
DISC_SNS, DISC_SW = f"{PREFIX}/sensor/{DEVICE_ID}_action/config", f"{PREFIX}/switch/{DEVICE_ID}_aim/config"

sensor_payload = {
  "name": f"{DEVICE_NAME} Action",
  "state_topic": STATE_TOPIC,
  "value_template": "{{ value_json.action }}",
  "unique_id": f"{DEVICE_ID}_action",
  "device": {"identifiers":["homebase"],"name":"Homebase System","model":"Dummy Sentry","manufacturer":"Viztron"}
}
switch_payload = {
  "name": f"{DEVICE_NAME} Aim",
  "command_topic": CMD_TOPIC,
  "payload_on": json.dumps({"action":"aim"}),
  "payload_off": json.dumps({"action":"stop"}),
  "unique_id": f"{DEVICE_ID}_aim",
  "device": {"identifiers":["homebase"],"name":"Homebase System","model":"Dummy Sentry","manufacturer":"Viztron"}
}

def on_message(cli, _, msg):
    print("SENTRY CMD:", msg.payload.decode())
    action = json.loads(msg.payload).get("action","unknown")
    cli.publish(STATE_TOPIC, json.dumps({"action":action}), qos=1)

cli = mqtt.Client()
cli.username_pw_set(USER, PASS)
cli.connect(BROKER, 1883, 60)

cli.publish(DISC_SNS, json.dumps(sensor_payload), retain=True)
cli.publish(DISC_SW, json.dumps(switch_payload), retain=True)
cli.subscribe(CMD_TOPIC, qos=1)
cli.on_message = on_message

print(f"🔄  sentry_dummy listening on {CMD_TOPIC}")
cli.loop_forever()


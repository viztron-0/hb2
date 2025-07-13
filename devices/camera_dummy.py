# camera_dummy.py
#!/usr/bin/env python3
import paho.mqtt.client as mqtt, json

PREFIX, DEVICE_ID, DEVICE_NAME = "homeassistant", "camera_front_door", "Front Door Camera"
BROKER, USER, PASS = "127.0.0.1", "mqtt_user", "password"
CMD_TOPIC, STATE_TOPIC = "homebase/camera/front_door/cmd","homebase/camera/front_door/status"
DISC_SNS, DISC_SW = f"{PREFIX}/sensor/{DEVICE_ID}_speaker/config", f"{PREFIX}/switch/{DEVICE_ID}_speak/config"

sensor_payload = {
  "name": f"{DEVICE_NAME} Speaker Action",
  "state_topic": STATE_TOPIC,
  "value_template": "{{ value_json.speaker_action }}",
  "unique_id": f"{DEVICE_ID}_speaker",
  "device": {"identifiers":["homebase"],"name":"Homebase System","model":"Dummy Camera","manufacturer":"Viztron"}
}
switch_payload = {
  "name": f"{DEVICE_NAME} Speak",
  "command_topic": CMD_TOPIC,
  "payload_on": json.dumps({"action":"speak"}),
  "payload_off": json.dumps({"action":"stop_speak"}),
  "unique_id": f"{DEVICE_ID}_speak",
  "device": {"identifiers":["homebase"],"name":"Homebase System","model":"Dummy Camera","manufacturer":"Viztron"}
}

def on_message(cli, _, msg):
    print("CAMERA CMD:", msg.payload.decode())
    action = json.loads(msg.payload).get("action","unknown")
    cli.publish(STATE_TOPIC, json.dumps({"speaker_action":action}), qos=1)

cli = mqtt.Client()
cli.username_pw_set(USER, PASS)
cli.connect(BROKER, 1883, 60)

cli.publish(DISC_SNS, json.dumps(sensor_payload), retain=True)
cli.publish(DISC_SW, json.dumps(switch_payload), retain=True)
cli.subscribe(CMD_TOPIC, qos=1)
cli.on_message = on_message

print(f"🔄  camera_dummy listening on {CMD_TOPIC}")
cli.loop_forever()


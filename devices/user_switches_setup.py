#!/usr/bin/env python3
import paho.mqtt.client as mqtt, json

BROKER, USER, PASS = "127.0.0.1", "mqtt_user", "password"
disc = [
  ("confirm_fire", "Confirm Fire", "homebase/user/confirm_fire", {"yes": True}),
  ("call_police",  "Call Police",  "homebase/user/call_police",  {"call": True})
]

cli = mqtt.Client()
cli.username_pw_set(USER, PASS)
cli.connect(BROKER, 1883, 60)

for obj_id, name, cmd_t, payload in disc:
    topic = f"homeassistant/switch/{obj_id}/config"
    cfg = {
      "name": name,
      "command_topic": cmd_t,
      "payload_on":  json.dumps(payload),
      "payload_off": json.dumps({}),
      "unique_id": obj_id,
      "optimistic": True
    }
    cli.publish(topic, json.dumps(cfg), retain=True)
    print("Published discovery:", topic)

cli.disconnect()


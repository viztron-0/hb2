#!/usr/bin/env python3
import os, json, time
import paho.mqtt.client as mqtt
from yolox.tracker.byte_tracker import BYTETracker   # already in image
from yolox.utils.demo_utils import letterbox
import cv2, numpy as np

# ----- ENV -----
MQTT_HOST = os.getenv("MQTT_HOST", "127.0.0.1")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
IN_TOPIC  = os.getenv("IN_TOPIC",  "frigate/events")
OUT_TOPIC = os.getenv("OUT_TOPIC", "homebase/tracks")
CONF_MIN  = float(os.getenv("CONF_MIN", "0.4"))

tracker = BYTETracker(track_thresh=CONF_MIN)
client = mqtt.Client()

if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_HOST)

def on_msg(_, __, msg):
    data = json.loads(msg.payload)
    if data.get("type") != "new":
        return
    box = data["after"]["box"]            # [x1,y1,x2,y2]
    conf = data["after"]["score"]
    w, h = data["after"]["frame"]["width"], data["after"]["frame"]["height"]
    # fake detections array for tracker: [[x1,y1,x2,y2,conf,cls]]
    dets = np.array([[*box, conf, 0]])
    online_targets = tracker.update(dets, (h, w), (w, h))
    for t in online_targets:
        x1,y1,x2,y2,track_id = *t.tlbr, t.track_id
        payload = {
            "track_id": int(track_id),
            "camera":   data["after"]["camera"],
            "bbox":     [float(x1),float(y1),float(x2),float(y2)],
            "centroid": [float((x1+x2)/2), float((y1+y2)/2)],
            "confidence": float(conf),
            "timestamp": time.time()
        }
        client.publish(OUT_TOPIC, json.dumps(payload), qos=0, retain=False)

client.on_message = on_msg
client.subscribe(f"{IN_TOPIC}/#")
client.loop_forever()


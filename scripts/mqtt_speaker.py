import paho.mqtt.client as mqtt
import json
import os
from gtts import gTTS  # comment out if using espeak

BROKER = "127.0.0.1"
USER = "mqtt_user"
PASS = "password"
TOPIC = "homebase/camera/front_door/cmd"

def speak(text):
    print(f"🗣️ Speaking: {text}")
    # Method A: gTTS
    tts = gTTS(text)
    tts.save("/tmp/speak.mp3")
    os.system("mpg123 /tmp/speak.mp3")

    # Method B: espeak
    # os.system(f'espeak "{text}"')

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        if payload.get("action") == "speak":
            message = payload.get("message", "No message")
            speak(message)
    except Exception as e:
        print(f"⚠️ Error: {e}")

client = mqtt.Client()
client.username_pw_set(USER, PASS)
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC, qos=1)
client.on_message = on_message

print(f"🔊 Listening on '{TOPIC}'...")
client.loop_forever()


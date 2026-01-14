#!/usr/bin/env python3
"""
Raspberry Pi Volume MQTT Interface
- Listens for volume commands from Home Assistant
- Publishes volume status periodically
- Supports Home Assistant MQTT Auto-Discovery
"""

import os
import sys
import time
import json
import random
import paho.mqtt.client as mqtt
import alsaaudio


DISCOVERY_SEEN = False
VERSION = "2026.01.10"
CONFIG_FILE = "rpi_volume.conf"
BROKER_ADDRESS = ""

TEN_MINUTES = 600
RANDOM_JITTER = random.randint(0, 60)

# MQTT topics (filled after loading computer name)
DISCOVERY_TOPIC = None

# State
PI_VOLUME = None
VOLUME_LEVEL = 0
LAST_UPDATE = 0
COMPUTER = ""

def load_config():
    """ This loads the comfigureatio info
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file '{CONFIG_FILE}' not found.")

    with open(CONFIG_FILE, "r") as vol_config:
        data = json.load(vol_config)
        print(data)
    # Optional: sanity checks
    if "broker_address" not in data or "computer_name" not in data:
        raise ValueError("Config file missing required fields.")

    return data

def publish_discovery(client, computer_name):
    """
    # ------------------------------------------------------------
    # MQTT Auto-Discovery
    # ------------------------------------------------------------
    """
    payload = {
        "name": computer_name + " Volume",
        "unique_id": computer_name + "_volume_control",
        "brightness_command_topic": "rpi/volume/" + computer_name + "/set",
        "command_topic": "rpi/volume/" + computer_name + "/set",
        "brightness_state_topic": "rpi/volume/" + computer_name + "/status",
        "brightness": True,              # HA uses brightness slider for volume
        "brightness_scale": 100,
        "qos": 0,
        "on_command_type": 'brightness',
        "device": {
            "identifiers": [computer_name + "_pi"],
            "name": computer_name + " Raspberry Pi",
            "manufacturer": "Raspberry Pi Foundation",
            "model": "Volume Controller",
            "sw_version": VERSION
        }
    }

    client.publish(DISCOVERY_TOPIC, json.dumps(payload), retain=True)
    print("Published Home Assistant discovery config")


def on_connect(client, _userdata, _flags, result_code):
    """
    # ------------------------------------------------------------
    # MQTT Callbacks
    # ------------------------------------------------------------
    """

    global DISCOVERY_SEEN # pylint: disable=global-statement
    print("Connected to MQTT broker with result:", result_code)
    client.subscribe(DISCOVERY_TOPIC)
    #client.subscribe("rpi/volume/" + computer + "/#")


def on_message(client, _userdata, msg):
    """
    Received data processing
    """
    global VOLUME_LEVEL, LAST_UPDATE, PI_VOLUME, COMPUTER, DISCOVERY_SEEN # pylint: disable=global-statement
    new_value = VOLUME_LEVEL
    try:
        payload = msg.payload.decode("utf-8", "ignore")
        if msg.topic.endswith("/config"):
            DISCOVERY_SEEN = True
            print("Discovery" + str(DISCOVERY_SEEN))
        if msg.topic == "rpi/volume/" + COMPUTER + "/set":
            new_value = int(payload)
            print(int(payload))
            if new_value != VOLUME_LEVEL:
                VOLUME_LEVEL = new_value
                PI_VOLUME.setvolume(VOLUME_LEVEL)
                publish_status(client)
                print("set new Volume")
            else:
                print("err " + str(new_value) + "--" + str(VOLUME_LEVEL))
        print(msg.topic)
        print(payload)
    except ValueError as errmsg:
        print(f"Invalid payload {msg.payload!r}: {errmsg}")
        return

def publish_status(client):
    """
    # ------------------------------------------------------------
    # Publish status
    # ------------------------------------------------------------
    """
    global LAST_UPDATE, VOLUME_LEVEL, PI_VOLUME, COMPUTER # pylint: disable=global-statement

    try:
        mixer_name = alsaaudio.mixers()[0]
        PI_VOLUME = alsaaudio.Mixer(mixer_name)
        VOLUME_LEVEL = int(PI_VOLUME.getvolume()[0])
        client.publish("rpi/volume/" + COMPUTER + "/status", VOLUME_LEVEL, retain=True)
        LAST_UPDATE = time.time()
    except Exception as errcode:
        print("MQTT publish error:", errcode)



def main():
    """
    # ------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------
    """
    global DISCOVERY_TOPIC, VOLUME_LEVEL, LAST_UPDATE, PI_VOLUME, BROKER_ADDRESS,\
           COMPUTER, DISCOVERY_SEEN # pylint: disable=global-statement
    config = load_config()

    BROKER_ADDRESS = config["broker_address"]
    COMPUTER = config["computer_name"]

    print("Loaded config:")
    print("  Broker:", BROKER_ADDRESS)
    print("  computer:", COMPUTER)
    DISCOVERY_TOPIC = "homeassistant/light/" + COMPUTER + "_volume/config"

    # Initialize ALSA mixer
    try:
        mixer_name = alsaaudio.mixers()[0]
        PI_VOLUME = alsaaudio.Mixer(mixer_name)
        VOLUME_LEVEL = int(PI_VOLUME.getvolume()[0])
        #print(f"Using ALSA mixer: {mixer_name}")
    except Exception as errcode:
        print("ALSA error:", errcode)
        sys.exit(1)

    # MQTT setup
    client = mqtt.Client(COMPUTER + "/volume/")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS)
    client.loop_start()
    time.sleep(2)

    # Publish discovery + initial state
    if not DISCOVERY_SEEN:
        print("Discovery" + str(DISCOVERY_SEEN))
        computer_name = COMPUTER
        publish_discovery(client, computer_name)
    client.subscribe("rpi/volume/" + COMPUTER + "/#")
    publish_status(client)

    # Main loop
    while True:
        now = time.time()
        mixer_name = alsaaudio.mixers()[0]
        involume = alsaaudio.Mixer(mixer_name)
        #print(int(VOLUME_LEVEL) == int(inVolume.getvolume()[0]))

        if  int(VOLUME_LEVEL) != int(involume.getvolume()[0]):
            print("VOLUME_LEVEL=" + str(int(involume.getvolume()[0])))
            print("got_" + str(involume.getvolume()[0]))
            VOLUME_LEVEL = int(involume.getvolume()[0])
            client.publish("rpi/volume/" + COMPUTER + "/set", \
            int(involume.getvolume()[0]), retain=True)
            client.publish("rpi/volume/" + COMPUTER + "/status", \
            int(involume.getvolume()[0]), retain=True)
            # # publish_status(client)

        # Periodic update every 10 minutes + jitter
        if now - LAST_UPDATE > (TEN_MINUTES + RANDOM_JITTER):
            publish_status(client)

        time.sleep(1)


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

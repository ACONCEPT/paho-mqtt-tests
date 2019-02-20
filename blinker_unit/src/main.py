import paho.mqtt.client as mqtt
import time
import sys
import json
import os
import socket
import random as rd

#broker_address="192.168.1.12"
broker_address="localhost"
mqttclient = mqtt.Client()

pid = os.getpid()
hostname = socket.gethostbyname(socket.gethostname())
config = {"delay":3}

def connect_client():
    mqttclient.connect(broker_address)

def on_connect(client, userdata, flags, rc):
    print("blinker client connected")
    client.subscribe("blinker")

def blinker_callback_state(blinker_state = False,feedback_topic = "test/responses"):

    def msg_callback(client, userdata, msg):
        print("in callback")
        msgjson = json.loads(msg.payload)
        print("msgjson {}".format(msgjson))
        cmd = msgjson.get("state_change")
        nonlocal blinker_state
        try:
            if cmd == "turn-on" and not blinker_state:
                print("turning on")
                blinker_state = True
                client.publish(feedback_topic,
                                json.dumps({"action":"turn-on"}))
            elif cmd == "turn-off" and blinker_state:
                print("turning off")
                blinker_state = False
                client.publish(feedback_topic,
                                json.dumps({"action":"turn-off"}))
            elif cmd == "turn-on" and blinker_state:
                print("already on")
                client.publish(feedback_topic,
                                json.dumps({"action":"nothing"}))
            elif cmd == "turn-off" and not blinker_state:
                print("already off")
                client.publish(feedback_topic,
                                json.dumps({"action":"nothing"}))
        except Exception as e:
            print("exception in switch {}".format(e))
    return msg_callback

def blink():
    print("blinker connecting to broker {}".format(broker_address))
    topic = "blinker"
    client = mqttclient
    client.on_connect = on_connect
    client.on_message = blinker_callback_state()
    client.connect(broker_address)
    client.loop_forever()

#class Blinker(object):
#    def __init__(self,broker_address = "localhost",blinker_channel = "blinker"):
#        self.channel = blinker_channel
#        self.client = mqttclient
#        self.client.on_connect = on_connect
#        self.client.on_message = msg_callback
#        print("connecting to broker @ host {}".format(broker_address))
#        self.client.connect(broker_address)
#
#    def run(self):
#        print("looping")
#        self.blinker_state = "off"
#        self.client.loop_forever()
#        print("after loop forever")
#
#blinker = Blinker()
#def run_blinker():
#    blinker.run()


def delay_start(delay):
    for i in range(delay):
        time.sleep(1)
        print("sending from host {}, pid {} in {}".format(hostname,pid,(delay) - i))

def turn_on():
    blinker_msg({"state_change":"turn-on"})

def turn_off():
    blinker_msg({"state_change":"turn-off"})

def blinker_msg(payload,topic = "blinker"):
    print("sending message {} to {}".format(payload, topic))
    connect_client()
    mqttclient.publish(topic,json.dumps(payload),1)
    mqttclient.loop()

if __name__ == "__main__":
    #delay_start(config.get("delay"))
    command = sys.argv[1]
    module = sys.modules[__name__]
    run = sys.argv[1]
    print("activating {}".format(run))
    getattr(module,run)()

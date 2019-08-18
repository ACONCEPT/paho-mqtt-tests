import paho.mqtt.client as mqtt
import time
import sys
import os
import socket
import random as rd
import json

broker_address="192.168.1.14"
#broker_address="localhost"
client = mqtt.Client()
client.connect(broker_address, 1883, 60)

# Read from all files
count = 0
reps = 3
pid = os.getpid()
hostname = socket.gethostbyname(socket.gethostname())
for i in range(reps):
    time.sleep(1)
    print("sending from host {}, pid {} in {}".format(hostname,pid,(reps) - i))

#topic = "test/{}".format(sys.argv[1])
topic = "blinker"
for i in range(20):
    payload = {}
    payload["state"] = "on"
    #payload = "test-message:i:{}".format(i)
    client.publish(topic, json.dumps(payload), 1)
    client.loop()
    print("sent payload {} to topic {}".format(payload,topic))
    count = count+1
    time.sleep(rd.randint(0,5))

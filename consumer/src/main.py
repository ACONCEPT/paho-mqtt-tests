import paho.mqtt.client as mqtt
import sys

#topic = "test/{}".format(sys.argv[1])
topic = "blinker"

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    #client.subscribe("$SYS/broker/clients/connected")
    client.subscribe(topic)
    client.subscribe("test/#")


def on_message(client, userdata, msg):
    print("topic : {} || payload : {}".format(msg.topic,str(msg.payload)))
#broker_address = "192.168.1.12"
broker_address = "localhost"

subclient = mqtt.Client()
subclient.on_connect = on_connect
subclient.on_message = on_message
subclient.connect(broker_address)
subclient.loop_forever()

#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import random, time



thisdict =    {
  "30:52:cb:fc:d0:29": (1,2,"08","22"),
  "dc:a6:32:5c:c0:a0": (2,1,"07","23"),
  "dc:a6:32:5c:c0:a1": (3,15,"08","22"),
  "dc:a6:32:5c:c0:a2":(4,20,"08","22")
}


broker = "192.168.87.135"
#broker ="test.mosquitto.org"
port = 1883
topic_client = "/camerasystem2/surveillance/+/"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
qos = 2



# This is the Subscriber
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_client)


def on_message(client, userdata, msg):
    global variables
    message = str(msg.payload.decode())
    print(message)
    if message in thisdict:
        variables = thisdict[message]
    else:
        pass
    on_publish(client, userdata, msg)

def on_publish(client,userdata,msg):
    client.unsubscribe(topic_client)
    msgkomnu = str(msg.payload.decode())
    topic_publish = str("/camerasystem1/surveillance/data/"+msgkomnu+"/")
    client.subscribe(topic_publish)
    time.sleep(1)
    msg = str(variables)
    result = client.publish(topic_publish, msg, qos)
    # result: [0, 1]
    status = result[0]
    print(status)
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_publish}`")
    else:
        print(f"Failed to send message to topic {topic_publish}")
    client.unsubscribe(topic_publish)
    client.subscribe(topic_client)


client = mqtt.Client()
client.connect(broker, 1883)
client.on_connect = on_connect
client.on_message = on_message

while True:
    client.loop_start()




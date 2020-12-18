import time
import os
import random
import base64
import paho.mqtt.client as mqtt
from getmac import get_mac_address as gma
from datetime import datetime


broker ="192.168.87.135"
port = 1883
topic_client = "/camerasystem1/surveillance/data/"+gma()+"/"
topic_mac = "/camerasystem2/surveillance/"+gma()+"/"
topic_capture = "/location/pi/cam/"+gma()+"/"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
path = "/home/pi/Desktop/"
qos = 1
qos2 = 2
gmaright = gma() + "   "
gmabyte = bytes(gma(), "utf-8")
realtime = (datetime.now().strftime("%H"))
realtime1 = int(realtime)

def connect_mqtt():
    def on_connect(client,userdata,flags,rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port)

    client.subscribe(topic_client)
    return client

def publish_mac(client):
    client.unsubscribe(topic_client)
    client.subscribe(topic_mac)
    time.sleep(1)
    msg = gma()
    result = client.publish(topic_mac, msg, qos)
    status = result[0]
    print(status)
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_mac}`")
    else:
        print(f"Failed to send message to topic {topic}")
    client.unsubscribe(topic_mac)
    client.subscribe(topic_client)

def on_message(client, userdata, msg):
    global ID
    global Int
    global Period_start
    global Period_end

    client.subscribe(topic_client)
    message = str(msg.payload.decode())
    final_message = message.replace('(', "").replace(')', "").replace(" ", "").replace("'",'"').replace('"','')
    list = final_message.split(",")
    ID = (list[0])
    Int = (list[1])
    Period_start = (list[2])
    Period_end = (list[3])
    timer()

def timer():
    if Period_start < realtime and Period_end > realtime:
        run()
    if Period_start > realtime and Period_end < realtime:
        pass
    else:
        pass

def capture_image():
    os.system("fswebcam -r 640x480 pic.jpg -save"+path)

def encode_image():
    image_file = open(path + "pic.jpg", "rb+")
    encoded_string = base64.b64encode(image_file.read() + gmabyte)
    return encoded_string

def publish_capture(client):
    client.unsubscribe(topic_client)
    client.subscribe(topic_capture)
    msg1 = encode_image()
    result = client.publish(topic_capture, msg1, qos, retain=False)
    status = result[0]
    if status == 0:
        print (f"Send `{msg1}` to topic `{topic_capture}`")
    else:
        print (f"Failed to send message to topic {topic_capture}")


def timed_message():
    while True:
        client = connect_mqtt()
        publish_mac(client)
        time.sleep(60)

def deleteimage():
    os.remove("pic.jpg")
    print ("image deleted")


def main(client):
    client.on_message = on_message
    client.loop_start()
    timed_message()

def run():
    client = connect_mqtt()
    client.on_message = on_message
    capture_image()
    encode_image()
    publish_capture(client)
    deleteimage()
    time.sleep(60 * int(Int)) # interval in minuts

while True:
    client = connect_mqtt()
    main(client)











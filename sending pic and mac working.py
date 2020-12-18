# import libraries
import time
import os
import random
import base64
import paho.mqtt.client as mqtt
from getmac import get_mac_address as gma

broker ="192.168.87.135"
port = 1883
topic ="/location/pi/cam/"+gma()+"/"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
path = '/home/pi/Desktop/'
qos = 2
gmaright = gma() + "   "
gmabyte = bytes(gma(), "utf-8")

#time
interval = 15
#secounds cant go below 60 secounds 
period = 20 #minuts


def main():
    client = connect_mqtt()
    client.loop_start()
    capture_image()
    encode_image()
    connect_mqtt()
    publish(client)
    deleteimage()
    


def connect_mqtt():
    def on_connect(client,userdata,flags,rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def capture_image():
   
    os.system('fswebcam -r 640x480  pic.jpg -save'+path)


def encode_image():
    image_file = open(path+"pic.jpg", "rb+")
    encoded_string = base64.b64encode(image_file.read()+gmabyte)
    return encoded_string



def publish(client):
    time.sleep(1)
    msg1 = encode_image()
    result = client.publish(topic, msg1, qos, retain=False)
    status = result[0]
    if status == 0:
        print(f"Send `{msg1}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

        
def deleteimage():
    os.remove("pic.jpg")
    print("image deleted")
    
    
timeout = time.time() + 60*period   # x minutes from now

while True:
    main()
    time.sleep(interval) # x secounds from now
    endpoint = 0
    if endpoint == period or time.time() > timeout:
        break
    

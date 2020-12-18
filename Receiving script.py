import base64
import paho.mqtt.client as mqtt
import random
from datetime import datetime
import os

Path = "/home/emil/Desktop/cam/"
broker = "192.168.87.135"
port = 1883
topic = "/location/pi/cam/#"
client_id = f'python-mqtt-{random.randint(0, 1000)}'



# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Your are connected to the MQTT-Broker| rc = " + str(rc))
    else:
        print("Your are not connected to the MQTT-Broker| rc = " + str(rc))
    client.subscribe(topic, 2)

def on_message(client, userdata, msg):
    message = (msg.payload.decode())
    decoded_string = base64.b64decode(message)
    MACbyte = decoded_string[-17:]
    MACstring = str(MACbyte)
    macright = MACstring[-18:]
    macfinal = macright[:-1]

    print("Picture received from mac: " + macfinal)


    directory = Path + macfinal + "/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    pic_file = open(directory + datetime.now().strftime("DATE = %d_%m_%Y___TIME = %H:%M:%S.jpg"), "wb+")
    pic_file.write(decoded_string)
    pic_file.close()
    #print(message)




client = mqtt.Client()
client.connect(broker, 1883)

client.on_connect = on_connect
client.on_message = on_message


while True:
    client.loop()
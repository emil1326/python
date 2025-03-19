from os import error
import time
import paho.mqtt.client as mqtt  # type: ignore
from lcdController import lcdController
from scrutteurDigitalDHT import scrutteurDigitalDHT

localname = input("Nom local")
distantname = input("Nom distant")

hasSub = False

screen = lcdController(1)
# screen.setColorByName("blue")
time.sleep(0.2)
screen.setText("Test")

print("did test")
time.sleep(0.5)


# Callback function quand on connect successful
def on_connect(client, userdata, flags, rc, empty):
    print("Connected with result code " + str(rc))
    screen.setText("conn: " + str(rc))

    global hasSub
    hasSub = True


# Callback function quand on recoit
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    screen.setText(f"msg: {msg.payload.decode()}")
    print(f"Température de l'équipier: {msg.payload.decode()}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "emildevclientlionelgroulxkf1")
client.on_connect = on_connect
client.on_message = on_message

# => vas faire on_connect si sa marche
# faut metter le bon ip de la machine => faire ipconfig?
client.connect("192.168.137.1", 1883, 10)

client.loop_start()

topic = f"clg/kf1/{localname}/temp"
message = "Hello, MQTT!, test test"
client.publish(topic, message)


# send once la temperature, disable le endloop pour le faire non-stop

temp = scrutteurDigitalDHT(3)


def doTemp(value):
    tempstr = f"{value[0]} C"
    print(f"Température locale: {tempstr}")
    screen.setText(tempstr)
    client.publish(topic, tempstr)

    # temp.endLoop()


temp.setFuncOnCheck(doTemp)

temp.reSetCheckWaitTimeAndStart(1)


# get la temperature distante

print("wait for conn")
time.sleep(3)

if hasSub:
    client.subscribe(f"clg/kf1/{distantname}/temp")
else:
    print("Couldnt connect err")

input("EndProgram")

temp.endLoopImmediately()
client.loop_stop()
client.disconnect()

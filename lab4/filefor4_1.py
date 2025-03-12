import time
import paho.mqtt.client as mqtt  # type: ignore
from lab3.lcdController import lcdController
from lab3.scrutteurDigitalDHT import scrutteurDigitalDHT

localname = input("Nom local").lower()
distantname = input("Nom distant").lower()

hasSub = False

screen = lcdController(1)
screen.setColorByName("blue")
screen.setText("Test")

time.sleep(0.5)


# Callback function quand on connect successful
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    screen.setText("conn: " + str(rc))

    hasSub = True


# Callback function quand on recoit
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    screen.setText(f"msg: {msg.payload.decode()}")
    print(f"Température de l'équipier: {msg.payload.decode()}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# => vas faire on_connect si sa marche
client.connect("test.mosquitto.org", 1883, 10)

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

    temp.endLoop()


temp.setFuncOnCheck(doTemp)

temp.reSetCheckWaitTimeAndStart(1)


# get la temperature distante

if hasSub:
    client.subscribe(f"clg/kf1/{distantname}/temp")
else:
    print("Couldnt connect err")

input("EndProgram")

client.loop_stop()
client.disconnect()


# pas de verrou mortel possible puisquil ny a aucun verrou utuliser dans mon code?
# il est tout de meme possible que les 2 ne marche pas sil attende tout les 2 que lautre envois leur temperature mais sa serrait juste une mauvaise conception a se point

import time
import paho.mqtt.client as mqtt  # type: ignore
from lcdController import lcdController
from scrutteurDigitalDHT import scrutteurDigitalDHT

localname = input("Nom local").lower()
distantname = input("Nom distant").lower()

hasSub = None

screen = lcdController(1)

time.sleep(1)


screen.setText("This is a longggggg test")
time.sleep(1)
screen.setText("test", line=0)

time.sleep(1)

# screen.setColorByName("blue")
screen.setText("Test", line=0)
screen.setText("Test l 2", line=1)

time.sleep(1)

screen.setText("", line=0)
screen.setText("", line=1)

time.sleep(1)


# Callback function quand on connect successful
def on_connect(client, userdata, flags, rc, last):
    print("Connected with result code " + str(rc))
    screen.setText(f"conn: {str(rc)}", line=1)

    global hasSub
    hasSub = True


# Callback function quand on recoit
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    screen.clearText(False, False, True)
    screen.setText(f"msg: {msg.payload.decode()}", line=1)
    print(f"Température de l'equipier: {msg.payload.decode()}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "emildevclientlionelgroulxkf1")
client.on_connect = on_connect
client.on_message = on_message

# => vas faire on_connect si sa marche
client.connect("broker.hivemq.com", 1883, 200)

client.loop_start()

topic = f"clg/kf1/{localname}/temp"
message = "Hello, MQTT!, test test"
client.publish(topic, message)


# send once la temperature, disable le endloop pour le faire non-stop

temp = scrutteurDigitalDHT(3)


def doTemp(value):
    tempstr = f"{value[0]} C"
    print(f"Temperature locale: {tempstr}")
    screen.setText(tempstr, line=0)
    client.publish(topic, tempstr)

    # temp.endLoop()


temp.setFuncOnCheck(doTemp)

temp.reSetCheckWaitTimeAndStart(1)


# get la temperature distante

if hasSub is None:  # timeout pour checker si sa a connecter correctement
    time.sleep(5)

    if hasSub != True:
        hasSub = False

if hasSub:
    client.subscribe(f"clg/kf1/{distantname}/temp")
else:
    print("Couldnt connect err")

input("Resend")  # si pas le premier a le faire

temp.reSetCheckWaitTimeAndStart(1)

input("EndProgram")

client.loop_stop()
client.disconnect()
temp.endLoop()


# pas de verrou mortel possible puisquil ny a aucun verrou utuliser dans mon code?
# il est tout de meme possible que les 2 ne marche pas sil attende tout les 2 que lautre envois leur temperature mais sa serrait juste une mauvaise conception a se point

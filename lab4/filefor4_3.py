from os import error
import time
import paho.mqtt.client as mqtt  # type: ignore
from lcdController import lcdController
from scrutteurDigitalDHT import scrutteurDigitalDHT

localname = input("Nom local")
distantname = input("Nom distant")

subscription_mid = None
publish_mid = None

screen = lcdController(1)
screen.setColorByName("blue")
screen.setText("Test")

time.sleep(0.5)


# Callback function quand on connect successful
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    screen.setText("conn: " + str(rc))

    global subscription_mid
    subscription_mid = True


# Callback function quand on recoit
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    screen.setText(f"msg: {msg.payload.decode()}")
    print(f"Température de l'équipier: {msg.payload.decode()}")


def on_subscribe(client, userdata, mid, granted_qos):
    global subscription_mid
    print(f"Subscribed: {mid} {granted_qos}")

    if mid == subscription_mid:
        print("mid match")
        if granted_qos[0] == 1:
            print("QoS 1 granted")
        else:
            print("QoS not granted")
    else:
        print("mid does not match")


def on_publish(client, userdata, mid):
    global publish_mid
    print(f"Message published with mid: {mid}")
    if mid == publish_mid:
        print("Message mid match")
    else:
        print("Message mid does not match")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "emildevclientlionelgroulxkf1")
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish

# => vas faire on_connect si sa marche
# faut metter le bon ip de la machine => faire ipconfig?
# raise error("Pas implementer")
client.connect("192.168.1.x", 1883, 10)

client.loop_start()

# send once la temperature, disable le endloop pour le faire non-stop

temp = scrutteurDigitalDHT(3, True)


def doTemp(value):
    topic = f"clg/kf1/{localname}/temp"
    tempstr = f"{value[0]} C"
    print(f"Température locale: {tempstr}")
    screen.setText(tempstr)
    client.publish(topic, tempstr, qos=1)

    temp.endLoop()


temp.setFuncOnCheck(doTemp)

temp.reSetCheckWaitTimeAndStart(1)


# get la temperature distante

if subscription_mid is not None:
    # vas faire On_subscribe
    subscription_mid = client.subscribe(f"clg/kf1/{distantname}/temp", qos=1)
else:
    print("Couldnt connect err")

input("EndProgram")

client.loop_stop()
client.disconnect()

import time
import paho.mqtt.client as mqtt # type: ignore
from lab3.lcdController import lcdController

client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
screen = lcdController(1)

screen.setColorByName("blue")
screen.setText("Test")

time.sleep(.5)

screen.setText("conn: ")
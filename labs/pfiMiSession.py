from time import sleep
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController
from scruttationManager import scruttationManager
from scrutteurHysteresiqueDHT import scrutteurHysteresiqueDHT
import paho.mqtt.client as mqtt  # type: ignore

# declare manager

scrutManager = scruttationManager()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "emildevclientlionelgroulxkf1")

# declare hardware

# in

potentiometre = scrutteurAnalog(0)
button = scrutteurDigital(2)
tempHum = scrutteurHysteresiqueDHT(4)  # digital
movementSensor = scrutteurDigital(7)

# out

screen = lcdController(1)
lumiereChauffage = basicPortControlSystem(3, True)  # Rouge
lumiereDeshumidificateur = basicPortControlSystem(5, True)  # Bleu
lumiereMovement = basicPortControlSystem(6, True)  # vert => 10sec

# valeures

# cible => upper bound
# canRestart => lowerBound
# waittime => temps hysteresique entre states

tempCible = 20
tempCanRestart = 18
tempWaitTime = 5  # lower => test
tempCurr = 0

humCible = 50
humCanRestart = 55  # upper ici pcq on remove
humWaitTime = 5
humCurr = 0

timeOnMovment = 10  # time c allumer apres avoir vu du movement

currPage = 0  # 0 = see vals, 1 = mod temp, 2 = mod hum, 3 = mod le mod / quit
currMode = 0  # 0 = local, 1 = distant, 2 = quit
lastPotVal = 0

localname = "emil/pfimises/clg/kf1"
distantname = "other/pfimises/clg/kf1"

# test hardware

screen.setColorByName("white")
screen.setText("test - emil")

lumiereChauffage.pulseSync(2, 0.1, 0.2)
lumiereDeshumidificateur.pulseSync(2, 0.1, 0.2)
lumiereMovement.pulseSync(2, 0.1, 0.2)

potentiometre.doCheckOnce()
print(f"pot test val: {potentiometre.oldValue}")

button.doCheckOnce()
print(f"button ispressed: {button.isPressed}")

movementSensor.doCheckOnce()
print(f"someone near moved? {button.isPressed}")

input("test done")

# declare functions

# hardware


def onButtonPress():
    global currPage

    print("Clicked on button")

    # avant de update currpage on est encore sur la bonne selon le nb, donc pas besoin de faire -1 dessus

    # exit been choosen
    if currPage == 3 and currMode == 2:
        exitApp()

    # neep put in vals from pot in
    if currPage == 1 or currPage == 2:
        if currPage == 1:
            global tempCible
            tempCible = round(lastPotVal / 34.1)
        else:
            global humCible
            humCible = round(lastPotVal / 10.23)
        pass

    currPage = currPage + 1
    if currPage > 3:
        currPage = 0

    updateUI()


def onPotChange(value):
    global lastPotVal

    lastPotVal = value

    print(f"change val pot to: {value}")

    updateUI()


def onMotionDetected():
    # gets called quand le premier movement est detecter

    onMotionStillDetected()


def onMotionStillDetected():
    # flash once 10s at max light, si un autre se met pardessu sa change rien, juste instanci plus de thread todo fix that?
    lumiereMovement.pulseAsync(1, 10, 0, 1)


def onTempLowerBound(value):
    lumiereChauffage.changeState(1)

    onTempChanged(value)


def onTempUpperBound(value):
    lumiereChauffage.changeState(0)

    onTempChanged(value)


def onHumLowerBound(value):
    lumiereDeshumidificateur.changeState(0)

    onHumChanged(value)


def onHumUpperBound(value):
    lumiereDeshumidificateur.changeState(1)

    onHumChanged(value)


def onTempChanged(value):
    global tempCurr
    tempCurr = value
    if currPage - 1 == 0:
        updateUI()
    
    print(f"Temp changed {value}")


def onHumChanged(value):
    global humCurr
    humCurr = value
    if currPage - 1 == 0:
        updateUI()

    print(f"hum changed {value}")

# mqtt func


# Callback function quand on connect successful
def on_connect(client, userdata, flags, rc, last):
    print("Connected with result code " + str(rc))
    # screen.setText(f"conn: {str(rc)}", line=1)


# Callback function quand on recoit un message
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    # screen.clearText(False, False, True)
    # screen.setText(f"msg: {msg.payload.decode()}", line=1)
    # print(f"Température de l'equipier: {msg.payload.decode()}")

    if currPage == 0:
        updateUI()


# callback quand on se sub a un sujet
def on_subscribe(client, userdata, mid, granted_qos, rc):
    pass


# callback quand onviens de publish
def on_publish(client, userdata, mid, other, other2):
    pass


# software


def updateUI():
    screen.clearText()

    if currPage == 0:  # see data
        if currMode == 0:
            screen.setColorByName("green")
            screen.setText("curr data:")
            # limite le nb de char ici, faut les 2 aye moin de 5 char each
            screen.setText(f"t: {tempCurr}, h: {humCurr}", line=2)
        elif currMode == 1:
            screen.setColorByName("yellow")
            screen.setText("curr data:")
            screen.setText("data distant", line=2)
        else:
            # error here
            pass
        pass
    elif currPage == 1:  # change temp cible
        screen.setColorByName("orange")
        screen.setText(f"cur temp: {tempCible}")
        screen.setText(f"new temp: {round(lastPotVal / 34.1)}", line=2)
        pass
    elif currPage == 2:  # change hum cible
        screen.setColorByName("blue")
        screen.setText(f"cur hum: {humCible}")
        screen.setText(f"new hum: {round(lastPotVal / 10.23)}", line=2)
        pass
    elif currPage == 3:  # see other menu => local, distant, quit
        screen.setColorByName("gold")
        screen.setText(f"local dist quit")
        screen.setText(f"sel mod: {potValToMenu(lastPotVal)}", line=2)
        pass
    else:
        # error
        pass

    pass


def potValToMenu(value):
    if value < 250:
        return "local"
    elif value < 500:
        return "distant"
    elif value < 1050:
        return "quit"
    else:
        # error
        pass


# start monitoring

scrutManager.addScrutteur(movementSensor)
scrutManager.addScrutteur(tempHum)
scrutManager.addScrutteur(button)
scrutManager.addScrutteur(potentiometre)

scrutManager.monitor()

tempHum.lowerBoundTemp = tempCible
tempHum.upperBoundTemp = tempCanRestart
tempHum.waitTimeEntreStatesTemp = tempWaitTime

tempHum.lowerBoundHum = humCanRestart
tempHum.upperBoundHum = humCible
tempHum.waitTimeEntreStatesHum = humWaitTime

button.setFuncOnPress(onButtonPress)


# mqtt

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish

# client.username_pw_set("nomusager", "password")

# client.connect("broker.hivemq.com", 1883, 10)

# client.loop_start()

# link hardware functions

button.setFuncOnPress(onButtonPress)
potentiometre.setFuncOnChange(onPotChange)

tempHum.setFuncOnLowerBoundTemp(onTempLowerBound)
tempHum.setFuncOnMiddleBoundTemp(onTempChanged)
tempHum.setFuncOnUpperBoundTemp(onTempUpperBound)
tempHum.setFuncOnLowerBoundHum(onHumLowerBound)
tempHum.setFuncOnMiddleBoundHum(onHumChanged)
tempHum.setFuncOnUpperBoundHum(onHumUpperBound)

movementSensor.setFuncOnPress(onMotionDetected)
movementSensor.setFuncOnHold(onMotionStillDetected)

# wait for end


# faut le mettre avant le wait TwT
def exitApp():
    client.loop_stop()
    client.disconnect()

    scrutManager.endLoopImmediately()

    lumiereChauffage.shutDown()
    lumiereDeshumidificateur.shutDown()
    lumiereMovement.shutDown()

    screen.shutDown()


print()
print("Finir?")
print()
input()

# finish

exitApp()

# ==> in work


# todo

# functions ??
# distant get/send

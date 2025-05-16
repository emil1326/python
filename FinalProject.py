from GPIOPort.basicPortControlSystemGPIO import basicPortControlSystemGPIO
from GPIOPort.scrutteurDigitalGPIO import scrutteurDigitalGPIO
from Pathing import martices
from Pathing.dijkatras import EmilsDijkatrasAlg
from gpiovoiture.robot import Robot

floor = martices.matrice_distances_floor
cooridinates = martices.matrice_distances_floor_coordinates

# software

dijkstraObject = EmilsDijkatrasAlg(floor)

# hardware

irSensorLeft = scrutteurDigitalGPIO(8)
irSensorRight = scrutteurDigitalGPIO(25)

voiture = Robot()

# consants

speedMul = 0.5  # 1 * speedMul = puissance
speedMulLeft = 1
speedMulRight = 1

entryPoint = 0  # start
outputPoint = 1  # finish

# variables

leftStatus = False
rightStatus = False

currentOrder = 0
moveOrders = ["left", "right", "forward"]

# hardWareFunctions


def sensorIsLeft():
    global leftStatus
    leftStatus = True


def sensorIsLeftNo():
    global leftStatus
    leftStatus = False


def sensorIsRight():
    global leftStatus
    leftStatus = True


def sensorIsRightNo():
    global leftStatus
    leftStatus = False


# check loop


# basically le main loop, juste mis dans un des capteures pour sa soit plus performant
def checkLoop():
    global speedMulLeft, speedMulRight, speedMul

    # Reset speed multipliers to default
    speedMulLeft = 1
    speedMulRight = 1
    speedMul = 0.5

    # on left line
    if leftStatus:
        speedMulRight = 0.1
    # on right line
    if rightStatus:
        speedMulLeft = 0.1
    # 2 line => intersection => check action list
    if leftStatus and rightStatus:
        speedMul = 0

    setSpeeds()


def setSpeeds():
    speedL = 1 * speedMul * speedMulLeft
    speedR = 1 * speedMul * speedMulRight

    voiture.setOnForTime(speedL, False, None, "left")
    voiture.setOnForTime(speedR, False, None, "right")

    if speedL == 0 and speedR == 0:
        voiture.arreter()


# link hardware functions

irSensorLeft.setFuncOnRelease(sensorIsLeft)
irSensorLeft.setFuncOnPress(sensorIsLeftNo)

irSensorRight.setFuncOnRelease(sensorIsRight)
irSensorRight.setFuncOnPress(sensorIsRightNo)

irSensorLeft.setFuncOnCheck(checkLoop)

# one time actions


def fillActionOrders():
    path, length = dijkstraObject.plus_court_chemin(entryPoint, outputPoint)
    print(f"Chemin trouve: {path}, longueur: {length}")

    global moveOrders
    moveOrders = []

    for i in range(1, len(path)):
        prev = path[i - 1]
        curr = path[i]

        prev_coord = cooridinates[prev]
        curr_coord = cooridinates[curr]

        dx = curr_coord[0] - prev_coord[0]
        dy = curr_coord[1] - prev_coord[1]

        if dx > 0:
            moveOrders.append("right")
        elif dx < 0:
            moveOrders.append("left")
        elif dy > 0:
            moveOrders.append("forward")
        elif dy < 0:
            moveOrders.append("backward")  # ==> turn twice, not used
        else:
            moveOrders.append("stay")  # au cas ou

    print(f"moveOrders: {moveOrders}")


fillActionOrders()

# start monitoring

irSensorLeft.monitor()
irSensorRight.monitor()

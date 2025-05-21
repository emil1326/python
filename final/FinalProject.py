import time
from scrutteurDigitalGPIO import scrutteurDigitalGPIO
import martices
from dijkatras import EmilsDijkatrasAlg
from robot import Robot
from scruttationManager import scruttationManager

floor = martices.matrice_distances_floor
cooridinates = martices.matrice_distances_floor_coordinates

# software

dijkstraObject = EmilsDijkatrasAlg(floor)
manager = scruttationManager(True)
manager.checkWaitTime = 0.1

# hardware

irSensorLeft = scrutteurDigitalGPIO(23)
irSensorRight = scrutteurDigitalGPIO(24)

voiture = Robot()

# consants

speedMul = (
    0.25  # 1 * speedMul * speedMulLeftLine * speedMulLeftIntersection = puissance
)

entryPoint = 0  # start
outputPoint = 13  # finish

coolDownTime = 3  # temps qui attend avant de pouvoir refaire une nouvelle intersection
timeToTurn = 2  # le temps nessecaire pour passer a travers une intersection

# variables

speedMulLeftLine = 1
speedMulRightLine = 1

speedMulLeftIntersection = 1
speedMulRightIntersection = 1

leftStatus = False
rightStatus = False

currentOrder = 0
moveOrders = ["left", "right", "forward"]

timeLastIntersection = 0  # tiumeStamp de la derniere fois on a ete a une intersection

# hardWareFunctions


def sensorIsLeft():
    global leftStatus
    leftStatus = False


def sensorIsLeftNo():
    global leftStatus
    leftStatus = True


def sensorIsRight():
    global rightStatus
    rightStatus = False


def sensorIsRightNo():
    global rightStatus
    rightStatus = True


# check loop


# basically le main loop, juste mis dans un des capteures pour sa soit plus performant
def checkLoop():
    global speedMulLeftLine, speedMulRightLine, speedMulLeftIntersection, speedMulRightIntersection, speedMul, currentOrder, timeLastIntersection

    # Reset speed multipliers to default
    speedMulLeftLine = 1
    speedMulRightLine = 1
    speedMulRightIntersection = 1
    speedMulLeftIntersection = 1

    useTime = False
    end = False

    # 2 line => intersection => check action list
    if leftStatus and rightStatus:

        currTime = time.perf_counter()
        # if coolDown time is done, can get a new order
        if currTime - timeLastIntersection > coolDownTime:
            print(
                f"Intersection! Attente écoulée: {currTime - timeLastIntersection} secondes"
            )
            currentOrder = currentOrder + 1
            if currentOrder >= len(moveOrders):
                # is finished
                speedMul = 0
                print("Is finished")
                manager.endLoop()
                voiture.shutdown()
                end = True
            else:
                print(
                    f"curr move order: {moveOrders[currentOrder]} at index: {currentOrder}"
                )

            timeLastIntersection = currTime

        if not end:
            if moveOrders[currentOrder] == "left":
                speedMulLeftIntersection = 0
            elif moveOrders[currentOrder] == "right":
                speedMulRightIntersection = 0
            elif moveOrders[currentOrder] == "forward":
                pass

        useTime = True

    # on left line
    elif leftStatus:
        speedMulLeftLine = 0.1
    # on right line
    elif rightStatus:
        speedMulRightLine = 0.1

    setSpeeds(useTime)


def setSpeeds(useTime):
    global speedMulLeftLine, speedMulRightLine, speedMulLeftIntersection, speedMulRightIntersection, speedMul, currentOrder, timeLastIntersection

    speedL = 1 * speedMul * speedMulLeftLine * speedMulLeftIntersection
    speedR = 1 * speedMul * speedMulRightLine * speedMulRightIntersection

    print(
        f"SetSpeeds at time : {time.time():.2f} : l {speedL:.3f} : r {speedR:.3f} -- l {leftStatus} : r {rightStatus}"
    )

    if useTime:
        if speedL == speedR:
            voiture.avancer(0.3, 1, True)
            voiture.arreter()
        else:
            voiture.setOnForTime(speedL, False, timeToTurn, "left")
            voiture.setOnForTime(speedR, False, timeToTurn, "right")
        # awaits que sa fini, vu que on est pas en exact time mode, sa va juste staller le reading des capteures( -> stall le manager ), donc se quon veut
        time.sleep(timeToTurn)
    else:
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
            moveOrders.append("stay")  # au cas ou, wont work
            raise Exception("invalid move")

    print(f"moveOrders: {moveOrders}")


fillActionOrders()

# start monitoring

manager.addScrutteur(irSensorLeft)
manager.addScrutteur(irSensorRight)

print("finish")

manager.monitor()

# wait for end

input()

# finish

manager.endLoop()
voiture.shutdown()


# ssh pi@192.168.137.199
# cd Documents/emilpyfile/final
# scp -r final pi@192.168.137.199:~/Documents/emilpyfile/
# cd C:\Users\emili\OneDrive - Collège Lionel-Groulx\SharedProjects\python

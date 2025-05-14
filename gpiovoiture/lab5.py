from robot import Robot

robot = Robot()

puissance = 0.5

robot.avancer(puissance, 2, True)

robot.turnR(puissance, 1, True)

robot.avancer(puissance, 2, True)

robot.turnL(puissance, 1, True)

robot.reculer(puissance, 2, True)

robot.turnR(puissance, 1, True)

robot.reculer(puissance, 2, True)

robot.turnL(puissance, 1, True)


# ssh pi@192.168.137.113
# cd Dexter/GrovePi/Software/Python/emilpyfile/labs/
# scp -r gpiovoiture pi@192.168.137.113:~/Documents/emilpyfile/
# cd C:\Users\emili\OneDrive - Collège Lionel-Groulx\SharedProjects\python

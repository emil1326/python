from rn import RadioNavigationSimple as TheRadioNavigationThatIsntTheFileOrTheClass
import cv2 # type: ignore
from dictKeyValue import MapTouches
from gab_robot import Robot
import numpy as np # type: ignore

IN1 = 5
IN2 = 6
ENA = 13

IN3 = 15
IN4 = 14
ENB = 18

robot = Robot(IN1, IN2, ENA, IN3, IN4, ENB)
rn = TheRadioNavigationThatIsntTheFileOrTheClass()
mapper = MapTouches(robot)

img = np.zeros((480, 480, 3), np.uint8)

maycontinue = rn.demarrer()#part la boucle seulement si demarrer a fonctionné
print('maycontinue: ', maycontinue)
while maycontinue:
    pos = rn.get_position()
    if(pos is not None):
        print('pos', pos[0], pos[1])
    
    cv2.imshow("test", img)
    #attendre une touche
    key = cv2.waitKeyEx(30)

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter
    if t == "x":
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")
    # mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(t)

#nettoyer le robot de tout ces processus
cv2.destroyAllWindows()
rn.arreter()
    
    
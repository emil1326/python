# algoritme de dyjkatras

import sys
from singleNode import singleNode as node


class EmilsDijkatrasAlg:

    inf = sys.maxsize

    def __init__(self, matrice_distance):
        self.__distances = matrice_distance

    def plus_court_chemin(self, depart, fin):
        if depart == fin:
            raise Exception("depart et fin sont le meme")
        if depart < 0 or depart >= len(self.__distances):
            raise Exception("depart invalide")
        if fin < 0 or fin >= len(self.__distances):
            raise Exception("fin invalide")

        # Initialiser la liste de noeuds
        noeuds = [node() for _ in range(len(self.__distances))]
        noeuds[depart].distance = 0

        while True:
            # Trouver noeud pas visite avec la plus petite distance
            curr_index = -1
            curr_distance = self.inf
            for i in range(len(noeuds)):
                if not noeuds[i].vu and noeuds[i].distance < curr_distance:
                    curr_distance = noeuds[i].distance
                    curr_index = i

            if curr_index == -1:
                break

            noeuds[curr_index].vu = True

            # dernier noeud
            if curr_index == fin:
                break

            for i, dist in enumerate(self.__distances[curr_index]):
                if dist != 0 and dist != self.inf and not noeuds[i].vu:
                    new_distance = noeuds[curr_index].distance + dist
                    if new_distance < noeuds[i].distance:
                        noeuds[i].distance = new_distance
                        noeuds[i].last = curr_index

        chemin = []
        curr = fin
        while curr is not None:
            chemin.insert(0, curr)
            curr = noeuds[curr].last

        if noeuds[fin].distance == self.inf:
            raise Exception("Aucun chemin trouvé")

        return chemin, noeuds[fin].distance

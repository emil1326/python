import sys
from singleNode import singleNode as node


class EmilsDijkatrasAlg:

    inf = sys.maxsize

    def __init__(self, matrice_distance):
        self.__distances = matrice_distance

    def plus_court_chemin(self, depart, fin):
        if depart == fin:
            raise Exception("depart et fin sont le meme")
        if depart < 0 or depart > fin:
            raise Exception("depart invalide")
        if fin > len(self.__distances):
            raise Exception("fin invalide")

        # Initialiser la liste de noeuds
        noeuds = []

        for i in range(len(self.__distances)):
            noeuds.append(node())
        noeuds[depart].distance = 0

        # Algorithme de Dijkstra
        foundEnd = False

        for i in range(len(self.__distances)):
            self.explore(noeuds[i], i)
            
            pass

    def explore(self, noeud, currNoeux):
        # pour toutes les distances dans le node
        for dist in self.__distances[currNoeux]:
            # discard wrong vals
            if dist == self.inf or dist == 0:
                return

            pass
        # gets node, check every non inf && non 0 relation of it, find shortest path
        # writes new lengths
        # returns all connections, in order of smallest to biggest
        return [2, 1]

        pass

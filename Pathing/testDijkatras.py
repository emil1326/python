# test file dijkraj

from dijkatras import EmilsDijkatrasAlg
from martices import matrice_distances_floor

Inf = EmilsDijkatrasAlg.inf

matrice_distances = matrice_distances_floor

pathing = EmilsDijkatrasAlg(matrice_distances)

path = pathing.plus_court_chemin(0, 13)

print("get")

input()

print(path)

input()
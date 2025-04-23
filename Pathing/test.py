from dijkatras import EmilsDijkatrasAlg

Inf = EmilsDijkatrasAlg.inf

matrice_distances = [
    [0, 3, 1, Inf, Inf, Inf],
    [3, 0, 1, 3, Inf, Inf],
    [1, 1, 0, 3, 5, Inf],
    [Inf, 3, 3, 0, 1, 3],
    [Inf, Inf, 5, 1, 0, 1],
    [Inf, Inf, Inf, 3, 1, 0],
]

pathing = EmilsDijkatrasAlg(matrice_distances)

print(pathing.plus_court_chemin(0, 5))

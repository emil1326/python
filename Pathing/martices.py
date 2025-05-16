# fichier pour garder les fichier de matrices ( pas faire le formatage tsu )

from dijkatras import EmilsDijkatrasAlg

Inf = EmilsDijkatrasAlg.inf

matrice_distances_test = [
    [0, 3, 1, Inf, Inf, Inf],
    [3, 0, 1, 3, Inf, Inf],
    [1, 1, 0, 3, 5, Inf],
    [Inf, 3, 3, 0, 1, 3],
    [Inf, Inf, 5, 1, 0, 1],
    [Inf, Inf, Inf, 3, 1, 0],
]

matrice_distances_floor = [
    #  1    2    3    4    5    6    7    8    9   10   11   12   13   14
    [  0,   2, Inf, Inf, Inf,   3, Inf, Inf, Inf, Inf, Inf, Inf, Inf, Inf],  # 1
    [  2,   0,   2, Inf, Inf, Inf, Inf, Inf, Inf, Inf, Inf, Inf, Inf, Inf],  # 2
    [Inf,   2,   0,   4, Inf, Inf,   2, Inf, Inf, Inf, Inf, Inf, Inf, Inf],  # 3
    [Inf, Inf,   4,   0, Inf, Inf, Inf, Inf,   2, Inf, Inf, Inf, Inf, Inf],  # 4
    [Inf, Inf, Inf, Inf,   0,   3, Inf, Inf, Inf,   2, Inf, Inf, Inf, Inf],  # 5
    [  3, Inf, Inf, Inf,   3,   0, Inf, Inf, Inf, Inf,   2, Inf, Inf, Inf],  # 6
    [Inf, Inf,   2, Inf, Inf, Inf,   0,   2, Inf, Inf, Inf, Inf,   4, Inf],  # 7
    [Inf, Inf, Inf, Inf, Inf, Inf,   2,   0,   2, Inf, Inf, Inf, Inf,   4],  # 8
    [Inf, Inf, Inf,   2, Inf, Inf, Inf,   2,   0, Inf, Inf, Inf, Inf, Inf],  # 9
    [Inf, Inf, Inf, Inf,   2, Inf, Inf, Inf, Inf,   0,   3,   8, Inf, Inf],  # 10
    [Inf, Inf, Inf, Inf, Inf,   2, Inf, Inf, Inf,   3,   0,   3, Inf, Inf],  # 11
    [Inf, Inf, Inf, Inf, Inf, Inf, Inf, Inf, Inf,   8,   3,   0,   2, Inf],  # 12
    [Inf, Inf, Inf, Inf, Inf, Inf,   4, Inf, Inf, Inf, Inf,   2,   0,   2],  # 13
    [Inf, Inf, Inf, Inf, Inf, Inf, Inf,   4, Inf, Inf, Inf, Inf,   2,   0],  # 14
]
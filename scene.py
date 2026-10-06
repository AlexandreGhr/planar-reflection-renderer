import numpy as np
from config import MIRROR_Y, WALL_Z

# Sol miroir
floor = {
    'name': 'floor',
    'vertices': np.array([
        [-50.0, MIRROR_Y, -50.0,  0, 1, 0,  0.0, 0.0],
        [ 50.0, MIRROR_Y, -50.0,  0, 1, 0,  1.0, 0.0],
        [ 50.0, MIRROR_Y,  50.0,  0, 1, 0,  1.0, 1.0],
        [-50.0, MIRROR_Y,  50.0,  0, 1, 0,  0.0, 1.0],
    ]),
    'triangles': np.array([[0, 1, 3], [1, 2, 3]], dtype=int),
    'normal': np.array([0, 1, 0]), # normale du plan miroir, pointe vers le haut (y+)
    'point': np.array([0, MIRROR_Y, 0]), # un point appartenant au plan miroir, utilisé pour le calcul de symétrie
    'color': np.array([0.2, 0.2, 0.2]),
}

# Mur miroir vertical
wall = {
    'name': 'wall',
    'vertices': np.array([
        [-5.0, -3.0, WALL_Z,  0, 0, 1,  0.0, 0.0],
        [ 5.0, -3.0, WALL_Z,  0, 0, 1,  1.0, 0.0],
        [ 5.0,  3.0, WALL_Z,  0, 0, 1,  1.0, 1.0],
        [-5.0,  3.0, WALL_Z,  0, 0, 1,  0.0, 1.0],
    ]),
    'triangles': np.array([[0, 1, 3], [1, 2, 3]], dtype=int),
    'normal': np.array([0, 0, 1]),
    'point': np.array([0, 0, WALL_Z]),
    'color': np.array([0.2, 0.4, 0.8]),
}

# Mur incliné à 45° (normale pointe vers le haut et vers la caméra)
N_tilted = np.array([0, 1, 1])
N_tilted = N_tilted / np.linalg.norm(N_tilted)  # normaliser

tilted = {
    'name': 'tilted',
    'vertices': np.array([
        [-5.0, -4.0, -3.0,  N_tilted[0], N_tilted[1], N_tilted[2],  0.0, 0.0],
        [ 5.0, -4.0, -3.0,  N_tilted[0], N_tilted[1], N_tilted[2],  1.0, 0.0],
        [ 5.0,  4.0, -1.0,  N_tilted[0], N_tilted[1], N_tilted[2],  1.0, 1.0],
        [-5.0,  4.0, -1.0,  N_tilted[0], N_tilted[1], N_tilted[2],  0.0, 1.0],
    ]),
    'triangles': np.array([[0, 1, 3], [1, 2, 3]], dtype=int),
    'normal': N_tilted,
    'point': np.array([0, -4, -3.0]),
    'color': np.array([0.25, 0.2, 0.3]),
}

mirrors = [floor, wall, tilted]
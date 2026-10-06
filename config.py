import numpy as np

# Effets optionnels
FRESNEL_ENABLED = True
ATTENUATION_ENABLED = False
POST_PROCESSING = False

# POSITION DU SOL (plan miroir)
MIRROR_Y = -1.5
WALL_Z = -2.0

# Type de miroir
MIRROR_MODE = 'surface'  # 'perfect' ou 'surface'

MIRROR_ROUGHNESS = 0.0  # 0.0 = miroir parfait, 1.0 = très flou

# Dimensions de l'image
WIDTH  = 1280
HEIGHT = 720

# Caméra


CAM_MODE = 3

if CAM_MODE == 0 : # Vue diagonale (un peu dessus + coté) -> SOL (Cam initale)
    CAMERA_POSITION = [1.1, 1.1, 1.1]
    CAMERA_LOOKAT   = [-0.577, -0.577, -0.577]
    CAMERA_UP       = np.array([0.33333333,  0.33333333, -0.66666667])
    CAMERA_RIGHT    = np.array([-0.57735027,  0.57735027,  0.])
elif CAM_MODE == 1: # MUR -> A GARDER
    CAMERA_POSITION = np.array([2.0, 0.0, 3.0])
    CAMERA_LOOKAT   = np.array([-0.55, 0.0, -0.83])
    CAMERA_UP       = np.array([0.0, 1.0, 0.0])
    CAMERA_RIGHT    = np.array([-0.83, 0.0, 0.55])
elif CAM_MODE == 2: # Wall
    CAMERA_POSITION = np.array([2.0, 0.0, 3.0])
    CAMERA_LOOKAT   = np.array([-0.55, 0.0, -0.83])
    CAMERA_UP       = np.array([0.0, 1.0, 0.0])
    CAMERA_RIGHT    = np.array([1.0, 0.0, 0.0])
elif CAM_MODE == 3: # Wall tilted / Wall
    CAMERA_POSITION = np.array([2.5, 0.0, 2.5])
    CAMERA_LOOKAT   = np.array([-0.707, 0.0, -0.707])
    CAMERA_UP       = np.array([0.0, 1.0, 0.0])
    CAMERA_RIGHT    = np.array([0.707, 0.0, -0.707])

# Position : (x,y,z) -> Position de la cam
# LookAt : (x,y,z) -> Ou regarde la cam
# UP : -> ou est le haut de la cam
# Right : -> Ou est la droite de la cam


# Projection
NEAR_PLANE   = 0.1

FAR_PLANE = 10.0
FOV          = 1.91986

# Lumière
LIGHT_POSITION = np.array([10, 0, 10])

# Facteur d'atténuation
ATTENUATION_FACTOR = 0.1

# Miroir activé
ACTIVE_MIRRORS = ['wall']
# ['floor', 'wall', 'tilted']

# Mode de comparaison
COMPARISON_MODE = 0

# Mode de sampling du reflet
# 'screen' : sampling direct (approximation)
# 'reproject' : reprojection via caméra virtuelle (précis)
REFLECTION_SAMPLING = 'screen'
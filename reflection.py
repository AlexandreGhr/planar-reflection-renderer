import numpy as np
from camera import Camera

def get_mirror_camera(cam, plane_normal, plane_point):
    N = plane_normal / np.linalg.norm(plane_normal)

    # Réflexion de la position
    pos = np.array(cam.position, dtype=float)
    pos_ref = pos - 2 * np.dot(pos - plane_point, N) * N

    # Réflexion des directions
    lookAt_ref = np.array(cam.lookAt) - 2 * np.dot(cam.lookAt, N) * N
    up_ref     = np.array(cam.up)     - 2 * np.dot(cam.up, N) * N
    right_ref  = np.array(cam.right)  - 2 * np.dot(cam.right, N) * N

    return Camera(pos_ref, lookAt_ref, up_ref, right_ref)
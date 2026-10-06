import numpy as np
from config import *
from graphicPipeline import GraphicPipeline
from camera import Camera
from projection import Projection
from reflection import get_mirror_camera
from readply import readply
from scene import mirrors
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt

# ----------------------------------------------------------------
# Chargement de la scène (commun à tous les comparatifs)
# ----------------------------------------------------------------
cam = Camera(CAMERA_POSITION, CAMERA_LOOKAT, CAMERA_UP, CAMERA_RIGHT)
proj = Projection(NEAR_PLANE, FAR_PLANE, FOV, WIDTH/HEIGHT)
vertices, triangles = readply('suzanne.ply')
image = asarray(Image.open('suzanne.png'))
active_mirrors = [m for m in mirrors if m['name'] in ACTIVE_MIRRORS]

def render_scene(cam, fresnelEnabled=False, attenuationEnabled=False, mirrorMode='perfect', roughness=0.0):
    pipe = GraphicPipeline(WIDTH, HEIGHT)

    cam_pos = cam.position if hasattr(cam, 'position') else CAMERA_POSITION
    data = dict([
        ('viewMatrix',        cam.getMatrix()),
        ('projMatrix',        proj.getMatrix()),
        ('cameraPosition',    cam_pos),
        ('lightPosition',     LIGHT_POSITION),
        ('texture',           image),
        ('attenuationFactor', ATTENUATION_FACTOR),
        ('fresnelEnabled',    fresnelEnabled),
        ('attenuationEnabled',attenuationEnabled),
        ('mirrorMode',        mirrorMode),
        ('roughness',         roughness),
        ('samplingMode', REFLECTION_SAMPLING),
    ])

    pipe.draw(vertices, triangles, data)

    floor_reflection = None
    for m in active_mirrors:
        camVirt = get_mirror_camera(cam, m['normal'], m['point'])
        pipeVirt = GraphicPipeline(WIDTH, HEIGHT)

        dataVirt = dict([
            ('viewMatrix',        camVirt.getMatrix()),
            ('projMatrix',        proj.getMatrix()),
            ('cameraPosition',    camVirt.position),
            ('lightPosition',     LIGHT_POSITION),
            ('texture',           image),
            ('attenuationFactor', ATTENUATION_FACTOR),
            ('fresnelEnabled',    fresnelEnabled),
            ('attenuationEnabled',attenuationEnabled),
            ('mirrorMode',        mirrorMode),
            ('roughness',         roughness),
        ])

        clip = (m['normal'], m['point'])
        pipeVirt.draw(vertices, triangles, dataVirt, True, clip_plane=clip)

        data['virtViewMatrix'] = camVirt.getMatrix()
        data['virtProjMatrix'] = proj.getMatrix()

        if m['name'] in ['floor', 'floor_grid']:
            floor_reflection = pipeVirt.image.copy()

        data['reflectionBuffer'] = pipeVirt.image
        data['mirrorColor'] = m['color']
        pipe.draw(m['vertices'], m['triangles'], data, mirror=True, cull=False)

    if POST_PROCESSING and floor_reflection is not None:
        empty_mask = ~pipe.stencilBuffer
        sol_color = np.array([0.0, 0.0, 0.0])
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if empty_mask[y, x]:
                    pipe.image[y, x] = 0.7 * floor_reflection[y, x] + 0.3 * sol_color

    return pipe.image

# ----------------------------------------------------------------
# COMPARATIF 0 : Sans réflexion / Avec réflexion
# ----------------------------------------------------------------
def comparatif_classic_planar():
    # Sans réflexion
    pipe_base = GraphicPipeline(WIDTH, HEIGHT)
    data_base = dict([
        ('viewMatrix',        cam.getMatrix()),
        ('projMatrix',        proj.getMatrix()),
        ('cameraPosition',    CAMERA_POSITION),
        ('lightPosition',     LIGHT_POSITION),
        ('texture',           image),
        ('attenuationFactor', 0.0),
        ('fresnelEnabled',    False),
        ('attenuationEnabled',False),
        ('mirrorMode',        'perfect'),
        ('roughness',         0.0),
    ])  # sans miroirs
    pipe_base.draw(vertices, triangles, data_base)

    # Avec réflexion
    img_avec = render_scene(cam, mirrorMode='perfect')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.imshow(np.clip(pipe_base.image, 0, 1))
    ax1.set_title("Base rendering")
    ax2.imshow(np.clip(img_avec, 0, 1))
    ax2.set_title("Planar reflection")
    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------------
# COMPARATIF 1 : Low Fresnel / High Fresnel
# ----------------------------------------------------------------
def comparatif_fresnel():
    # Caméra de face (Fresnel faible)
    cam_face = Camera(
        np.array([0.0, 0.0, -1.0]),  # entre Suzanne et le mur
        np.array([0.0, 0.0, -1.0]),  # regarde vers le mur
        np.array([0.0, 1.0, 0.0]),
        np.array([1.0, 0.0, 0.0])
    )

    cam_rasant = Camera(
        np.array([5.0, 0.0, -1.8]),  # très décalé en x, quasi au niveau du mur
        np.array([-0.99, 0.0, -0.14]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.14, 0.0, -0.99])
    )

    img_face   = render_scene(cam_face,   fresnelEnabled=True, mirrorMode='surface')
    img_rasant = render_scene(cam_rasant, fresnelEnabled=True, mirrorMode='surface')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.imshow(np.clip(img_face, 0, 1))
    ax1.set_title("Fresnel — face-on (weak reflection)")
    ax2.imshow(np.clip(img_rasant, 0, 1))
    ax2.set_title("Fresnel — grazing angle (strong reflection)")
    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------------
# COMPARATIF 2 : Décalage caméra
# ----------------------------------------------------------------
def comparatif_camera_offset():
    offsets = [-1.0, 0.0, 1.0, 2.0]
    base_pos   = np.array(CAMERA_POSITION, dtype=float)
    base_right = np.array(CAMERA_RIGHT,    dtype=float)

    fig, axes = plt.subplots(1, len(offsets), figsize=(5 * len(offsets), 5))
    for idx, offset in enumerate(offsets):
        pos = base_pos + offset * base_right
        cam_shift = Camera(pos, CAMERA_LOOKAT, CAMERA_UP, CAMERA_RIGHT)
        img = render_scene(cam_shift)
        axes[idx].imshow(np.clip(img, 0, 1))
        axes[idx].set_title(f"offset = {offset:.2f}")
        axes[idx].axis('off')

    plt.tight_layout()
    plt.show()


# ----------------------------------------------------------------
# COMPARATIF 3 : Sans roughness / Avec roughness
# ----------------------------------------------------------------
def comparatif_roughness():
    img_sans = render_scene(cam, mirrorMode='perfect', roughness=0.0)
    img_avec = render_scene(cam, mirrorMode='perfect', roughness=0.5)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.imshow(np.clip(img_sans, 0, 1))
    ax1.set_title("No roughness (roughness=0.0)")
    ax2.imshow(np.clip(img_avec, 0, 1))
    ax2.set_title("Roughness (roughness=0.5)")
    plt.tight_layout()
    plt.show()


# ----------------------------------------------------------------
# COMPARATIF 4 : Sans atténuation / Avec atténuation
# ----------------------------------------------------------------
def comparatif_attenuation(): # A FAIRE AVEC 10
    cam = Camera(
        np.array([2.5, 0.0, 2.5]),
        np.array([-0.707, 0.0, -0.707]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.707, 0.0, -0.707])
    )
    img_sans = render_scene(cam, mirrorMode='surface', attenuationEnabled=False)
    img_avec = render_scene(cam, mirrorMode='surface', attenuationEnabled=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.imshow(np.clip(img_sans, 0, 1))
    ax1.set_title("Sans atténuation")
    ax2.imshow(np.clip(img_avec, 0, 1))
    ax2.set_title(f"Avec atténuation (factor={ATTENUATION_FACTOR})")
    plt.tight_layout()
    plt.show()


# ----------------------------------------------------------------
# Lancement
# ----------------------------------------------------------------
if COMPARISON_MODE == 0: # Mettre le wall pour les comparatif
    comparatif_classic_planar()
elif COMPARISON_MODE == 1 : 
    comparatif_fresnel()
elif COMPARISON_MODE == 2:
    comparatif_camera_offset()
elif COMPARISON_MODE == 3:
    comparatif_roughness()
elif COMPARISON_MODE == 4:
    comparatif_attenuation()
else:
    print("Please set COMPARISON_MODE between 0 and 4 in config.py")

# ATTENTION A BIEN METTRE LE BON MIROIR POUR LES TESTS
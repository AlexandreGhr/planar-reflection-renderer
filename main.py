import numpy as np
from config import *
import time
from graphicPipeline import GraphicPipeline
from camera import Camera
from projection import Projection
from reflection import get_mirror_camera
from readply import readply
from scene import mirrors
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt

pipeline = GraphicPipeline(WIDTH, HEIGHT)

cam = Camera(CAMERA_POSITION, CAMERA_LOOKAT, CAMERA_UP, CAMERA_RIGHT)
proj = Projection(NEAR_PLANE, FAR_PLANE, FOV, WIDTH/HEIGHT)

vertices, triangles = readply('suzanne.ply')
image = asarray(Image.open('suzanne.png'))

data = dict([
    ('viewMatrix',     cam.getMatrix()),
    ('projMatrix',     proj.getMatrix()),
    ('cameraPosition', CAMERA_POSITION),
    ('lightPosition',  LIGHT_POSITION),
    ('texture',        image),
    ('attenuationFactor', ATTENUATION_FACTOR),
    ('fresnelEnabled', FRESNEL_ENABLED),
    ('attenuationEnabled', ATTENUATION_ENABLED),
    ('mirrorMode', MIRROR_MODE),
    ('roughness', MIRROR_ROUGHNESS),
    ('samplingMode', REFLECTION_SAMPLING),
])

start = time.time()

# Rendu de Suzanne (caméra réelle)
pipeline.draw(vertices, triangles, data)

floor_reflection = None

active_mirrors = [m for m in mirrors if m['name'] in ACTIVE_MIRRORS]
# Pour chaque miroir de la scène
for m in active_mirrors:
    # Caméra virtuelle (symétrie par rapport au plan du miroir)
    camVirt = get_mirror_camera(cam, m['normal'], m['point'])
    print(f"Mirror: {m['name']} | camVirt.position = {camVirt.position}")

    # Pipeline virtuelle pour ce miroir
    pipeVirt = GraphicPipeline(WIDTH, HEIGHT)

    dataVirt = dict([
        ('viewMatrix',     camVirt.getMatrix()),
        ('projMatrix',     proj.getMatrix()),
        ('cameraPosition', camVirt.position),
        ('lightPosition',  LIGHT_POSITION),
        ('texture',        image),
        ('attenuationFactor', ATTENUATION_FACTOR),
        ('fresnelEnabled',    FRESNEL_ENABLED),
        ('attenuationEnabled',ATTENUATION_ENABLED),
        ('mirrorMode', MIRROR_MODE),
        ('roughness', MIRROR_ROUGHNESS),
    ])

    # Rendu de la scène depuis la caméra virtuelle avec clip plane
    clip = (m['normal'], m['point'])
    pipeVirt.draw(vertices, triangles, dataVirt, True, clip_plane=clip) # clip_plane=clip

    data['virtViewMatrix'] = camVirt.getMatrix()
    data['virtProjMatrix'] = proj.getMatrix()

    # Sauvegarder le buffer du sol pour le post-processing
    if m['name'] in ['floor', 'floor_grid']:
        floor_reflection = pipeVirt.image.copy()

    # Passer le buffer de réflexion et la couleur du miroir
    data['reflectionBuffer'] = pipeVirt.image
    data['mirrorColor'] = m['color']

    # Rendu de la surface miroir
    pipeline.draw(m['vertices'], m['triangles'], data, mirror=True, cull=False)

# Post-processing
if POST_PROCESSING and floor_reflection is not None:
    empty_mask = ~pipeline.stencilBuffer
    sol_color = np.array([0.2, 0.2, 0.2])
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if empty_mask[y, x]:
                pipeline.image[y, x] = 0.7 * floor_reflection[y, x] + 0.3 * sol_color

end = time.time()
print(f"Temps: {end - start:.2f}s")

plt.imshow(np.clip(pipeline.image, 0, 1))
plt.title("Rendu final avec planar reflection")
plt.show()

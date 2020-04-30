import pygame
import pytmx
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer

pygame.init()
size = width, height = 1366, 768
from pytmx import TiledObjectGroup

#screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
tiled_map = pytmx.load_pygame('image\\Tilemap\\sample_urban.tmx')


for layer in tiled_map.visible_layers:
    if isinstance(layer, TiledTileLayer):
        print("TiledTileLayer")
        for x, y, image in layer.tiles():
            screen.blit(image, (x * 16, y * 16))
    elif isinstance(layer, TiledObjectGroup):
        print("TiledObjectGroup")
    elif isinstance(layer, TiledImageLayer):
        print("TiledImageLayer")

pygame.display.flip()

while True:
    pass
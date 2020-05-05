import pygame
import pytmx
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer
from pytmx import TiledMap

pygame.init()
size = width, height = 1366, 768
from pytmx import TiledObjectGroup

#screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
tiled_map = pytmx.load_pygame('image\\Tilemap\\t1.tmx')


for layer in tiled_map.visible_layers:
    print(layer)
    if isinstance(layer, TiledTileLayer):
        print("TiledTileLayer")
        # print(TiledMap.get_tile_properties(0, 0, layer))
        for t in layer.iter_data():
            if (t[2] != 0):
                print(tiled_map.get_tile_properties_by_gid(t[2]))
                print(t)
    elif isinstance(layer, TiledObjectGroup):
        print("TiledObjectGroup")
    elif isinstance(layer, TiledImageLayer):
        print("TiledImageLayer")

pygame.display.flip()

# while True:
#     pass
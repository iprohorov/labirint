import pygame

class Chest (pygame.sprite.Sprite): 
    def __init__ (self, X, Y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(X,Y))
    def clear_callback(surf, rect):
        color = 0, 0, 0
        surf.fill(color, rect)
    def do (self):
        
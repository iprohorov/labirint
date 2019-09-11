import pygame 

class Player: 
    def __init__ (self, X=16, Y=16):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.rect = self.image.get_rect(center=(X,Y))
import pygame 

class Player (pygame.sprite.Sprite): 
    def __init__ (self, X=16, Y=16, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(X,Y))
    def MoveLeft (self):
        self.rect.x -= 16 
    def MoveRight (self):
        self.rect.x += 16
    def MoveUp (self):
        self.rect.y -= 16
    def MoveDown (self):
        self.rect.y += 16
        

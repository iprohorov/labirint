import pygame 

class Player (pygame.sprite.Sprite): 
    def __init__ (self, X=16, Y=16, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(X,Y))
    def MoveLeft (self, Walls):
        self.rect.x -= 16 
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.x += 16 
    def MoveRight (self, Walls):
        self.rect.x += 16
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.x -= 16 
    def MoveUp (self, Walls):
        self.rect.y -= 16
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.y += 16 
    def MoveDown (self, Walls):
        self.rect.y += 16
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.y -= 16 
        

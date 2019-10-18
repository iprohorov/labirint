import pygame 

class Player (pygame.sprite.Sprite): 
    def __init__ (self, X=16, Y=16, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        imagesUPanimation = ["hero1z.png","hero2z.png","hero3z.png","hero4z.png"]
        self.loadedImage = []
        for imgName in imagesUPanimation:
            self.loadedImage.append(pygame.image.load(imgName).convert_alpha())
        self.currentFrame = len(self.loadedImage)-1
        self.image = self.loadedImage[self.currentFrame] 
        self.rect = self.image.get_rect(center=(X,Y))
        self.moving = False
        self.lastUpdateAnimationTime = 0
    def update(self):
        if (pygame.time.get_ticks()-self.lastUpdateAnimationTime)>500:
            self.currentFrame +=1
            self.lastUpdateAnimationTime = pygame.time.get_ticks()
        if self.currentFrame >= len(self.loadedImage): 
            self.currentFrame = 0
        print("frame {}".format(self.currentFrame))
        self.image = self.loadedImage[self.currentFrame] 

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
        

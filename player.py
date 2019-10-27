import pygame 

def LoadImageList (fileNamesList):
    imageList = []
    for fileName in fileNamesList:
        imageList.append(pygame.image.load(fileName).convert_alpha())
    return imageList



class Animation:
    def __init__ (self,framesFiles, frameTime):
        self.frames = LoadImageList (framesFiles)
        self.lastUpdateAnimationTime = 0
        self.currentFrame = 0
        self.frameTime = frameTime
        self.isPlay = False
    def isNeedApdate(self):
        if (pygame.time.get_ticks()-self.lastUpdateAnimationTime)>self.frameTime:
            self.currentFrame +=1
            self.lastUpdateAnimationTime = pygame.time.get_ticks()
            if self.currentFrame >= len(self.frames): 
                self.currentFrame = 0
            return True
        return False
    def getImg(self):
        if self.isPlay:
            self.isNeedApdate()
        return self.frames[self.currentFrame]
    def Start(self):
        self.isPlay = True
    def Stop(self):
        self.currentFrame = 0
        self.isPlay = False
    # add animation complete add time of animation 
        
class Player (pygame.sprite.Sprite):
    def __init__ (self, X=32, Y=32, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        self.upGoAnimation = Animation(["hero1z.png","hero2z.png","hero3z.png","hero4z.png"],500)
        self.currentAnimation = self.upGoAnimation
        self.image = self.currentAnimation.getImg()
        self.rect = self.image.get_rect(center=(X,Y))
        self.x_speed = 0
        self.y_speed = 0
        self.x:float = X
        self.y:float = Y
        self.privUpdateTime = 0

    def StopMoving(self):
        self.currentAnimation.Stop()
        self.x_speed = 0
        self.y_speed = 0 
    def update(self, Walls):
        dt = pygame.time.get_ticks() - self.privUpdateTime
        self.privUpdateTime = pygame.time.get_ticks()
        self.x += dt*self.x_speed
        self.y += dt*self.y_speed
        self.image = self.currentAnimation.getImg()
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            #self.x -= dt*self.x_speed+1
            #self.y -= dt*self.y_speed+1
            self.StopMoving()
        self.rect.x = self.x
        self.rect.y = self.y

    def MoveLeft (self):
        self.x_speed = -0.1
         
    def MoveRight (self):
        self.x_speed = 0.1
        
    def MoveUp (self):
        self.currentAnimation.Start()
        self.y_speed = -0.1
        
    def MoveDown (self):
        self.y_speed = 0.1
        
        

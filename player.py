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
    def __init__ (self, X=16, Y=16, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        self.upGoAnimation = Animation(["hero1z.png","hero2z.png","hero3z.png","hero4z.png"],500)
        self.currentAnimation = self.upGoAnimation
        self.image = self.currentAnimation.getImg()
        self.rect = self.image.get_rect(center=(X,Y))

    def update(self):
        self.image = self.currentAnimation.getImg()

    def MoveLeft (self, Walls):
        self.rect.x -= 16 
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.x += 16 
    def MoveRight (self, Walls):
        self.rect.x += 16
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.x -= 16 
    def MoveUp (self, Walls):
        self.currentAnimation.Start()
        self.rect.y -= 16
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.y += 16 
    def MoveDown (self, Walls):
        self.currentAnimation.Stop()
        self.rect.y += 16
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            self.rect.y -= 16 
        

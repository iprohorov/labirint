import pygame
import pygame.transform

def LoadImageList (fileNamesList):
    imageList = []
    for fileName in fileNamesList:
        imageList.append(pygame.image.load(fileName).convert_alpha())
    return imageList

class Animation:
    def __init__ (self,framesFiles, frameTime, flipX = False, flipY = False):
        self.frames = LoadImageList (framesFiles)
        self.lastUpdateAnimationTime = 0
        self.currentFrame = 0
        self.frameTime = frameTime
        self.isPlay = False
        self._Transform(flipX, flipY)
    def _Transform(self, flipX = False, flipY = False):
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.flip(frame, flipX, flipY)
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
        self.upGoAnimation = Animation(["hero1z.png","hero2z.png","hero3z.png","hero4z.png"],100)
        self.downGoAnimation = Animation(["herou1.png","herou2.png","herou3.png","herou4.png"],100)
        self.rightGoAnimation = Animation(["herol1.png","herol2.png","herol3.png","herol4.png"],100)
        self.leftGoAnimation = Animation(["herol1.png","herol2.png","herol3.png","herol4.png"],100, True)
        self.currentAnimation = self.downGoAnimation
        self.image = self.currentAnimation.getImg()
        self.rect = self.image.get_rect(center=(X,Y))
        self.x_speed = 0
        self.y_speed = 0
        self.x:float = X
        self.y:float = Y
        self.privUpdateTime = 0
        self.global_position_x = cameraPositionX+ int(self.x)
        self.global_position_y = cameraPositionY+ int(self.y)

    def StopMoving(self):
        self.currentAnimation.Stop()
        self.x_speed = 0
        self.y_speed = 0 
    def update(self, Walls, cameraPositionX, cameraPositionY):
        self.global_position_x = cameraPositionX+ int(self.x)
        self.global_position_y = cameraPositionY+ int(self.y)

        dt = pygame.time.get_ticks() - self.privUpdateTime
        self.privUpdateTime = pygame.time.get_ticks()
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0):
            if self.x_speed > 0:
                self.x -= 1
            elif self.x_speed < 0:
                self.x += 1
            if self.y_speed > 0:
                self.y -= 1
            elif self.y_speed < 0:
                self.y += 1
            self.StopMoving()
        else:
            self.x += dt*self.x_speed
            self.y += dt*self.y_speed
        self.image = self.currentAnimation.getImg()
        self.rect.topleft = (int(self.x), int(self.y))

    def MoveLeft (self):
        self.currentAnimation = self.leftGoAnimation 
        self.currentAnimation.Start()
        self.x_speed = -0.1
         
    def MoveRight (self):
        self.currentAnimation = self.rightGoAnimation 
        self.currentAnimation.Start()
        self.x_speed = 0.1
        
    def MoveUp (self):
        self.currentAnimation = self.upGoAnimation
        self.currentAnimation.Start()
        self.y_speed = -0.1
        
    def MoveDown (self):
        self.currentAnimation = self.downGoAnimation 
        self.currentAnimation.Start()
        self.y_speed = 0.1
        
class Mob (pygame.sprite.Sprite):
    def __init__ (self, x_start_global, y_start_global, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        self.upGoAnimation = Animation(["hero1z.png","hero2z.png","hero3z.png","hero4z.png"],100)
        self.downGoAnimation = Animation(["herou1.png","herou2.png","herou3.png","herou4.png"],100)
        self.rightGoAnimation = Animation(["herol1.png","herol2.png","herol3.png","herol4.png"],100)
        self.leftGoAnimation = Animation(["herol1.png","herol2.png","herol3.png","herol4.png"],100, True)
        self.currentAnimation = self.downGoAnimation
        self.image = self.currentAnimation.getImg()
        self.rect = self.image.get_rect(center=(0,0))
        self.isVisable = False  
        self.x_speed = 0
        self.y_speed = 0
        self.x:float = 0
        self.y:float = 0
        self.privUpdateTime = 0
        self.state = None
        self.global_position_x = x_start_global
        self.global_position_y = y_start_global
        
    def StopMoving(self):
        self.currentAnimation.Stop()
        self.x_speed = 0
        self.y_speed = 0 
    def update(self, Walls, player_x_sc, player_y_sc, cameraPositionX, cameraPositionY, size):
        width, height = size
        if not self.isVisable:
            if (cameraPositionX*16 < (self.global_position_x) <  cameraPositionX*16+width) and (cameraPositionY*16 < (self.global_position_y) <  cameraPositionY*16+height):
                self.isVisable = True
                self.x:float = self.global_position_x - cameraPositionX*16
                self.y:float = self.global_position_y - cameraPositionY*16

        if self.isVisable:
            if (self.global_position_x < cameraPositionX*16) or (self.global_position_x > cameraPositionX*16+width):
                self.isVisable = False 
            if (self.global_position_y < cameraPositionY*16) or (self.global_position_y > cameraPositionY*16+height):
                self.isVisable = False 

        if not self.isVisable:
            return -1 


        self.player_x_sc = player_x_sc
        self.player_y_sc = player_y_sc
        self.x = self.global_position_x - cameraPositionX*16
        self.y = self.global_position_y - cameraPositionY*16

        next_state = self.Intelect()
        if ((self.state is None) or (self.state != next_state)):
            print("Mob")
            self.state = next_state
            self.state()
        dt = pygame.time.get_ticks() - self.privUpdateTime
        self.privUpdateTime = pygame.time.get_ticks()
        if (len (pygame.sprite.spritecollide(self,Walls,False)) > 0): # add mobs
            if self.x_speed > 0:
                self.x -= 1
            elif self.x_speed < 0:
                self.x += 1
            if self.y_speed > 0:
                self.y -= 1
            elif self.y_speed < 0:
                self.y += 1
            self.StopMoving()
        else:
            self.x += dt*self.x_speed
            self.y += dt*self.y_speed
        self.image = self.currentAnimation.getImg()
        self.rect.x = self.x
        self.rect.y = self.y

        self.global_position_x = cameraPositionX*16+ self.x
        self.global_position_y = cameraPositionY*16+ self.y 
        return True 

    def MoveLeft (self):
        self.currentAnimation = self.leftGoAnimation 
        self.currentAnimation.Start()
        self.x_speed = -0.1
         
    def MoveRight (self):
        self.currentAnimation = self.rightGoAnimation 
        self.currentAnimation.Start()
        self.x_speed = 0.1
        
    def MoveUp (self):
        self.currentAnimation = self.upGoAnimation
        self.currentAnimation.Start()
        self.y_speed = -0.1
        
    def MoveDown (self):
        self.currentAnimation = self.downGoAnimation 
        self.currentAnimation.Start()
        self.y_speed = 0.1
    
    def Intelect (self): #return NextState
        if (self.player_x_sc - self.x > 32):
            return self.MoveRight
        elif (self.player_x_sc - self.x < -32):
             return self.StopMoving
        elif (self.player_y_sc - self.y > 32):
            return self.MoveDown
        elif (self.player_y_sc - self.y < -32):
            return self.MoveUp
        else:
            return self.StopMoving
        

        

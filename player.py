import pygame
import TimeObjects
import math
import pygame.transform

def LoadImageList (fileNamesList):
    imageList = []
    for fileName in fileNamesList:
        imageList.append(pygame.image.load(fileName).convert_alpha())
    return imageList

class Animation:
    def __init__ (self,framesFiles, frameTime, flipX = False, flipY = False, shot_animation = False):
        self.frames = LoadImageList (framesFiles)
        self.lastUpdateAnimationTime = 0
        self.currentFrame = 0
        self.frameTime = frameTime
        self.isPlay = False
        self.shot_animation = shot_animation
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
                if self.shot_animation:
                    self.Stop()
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
    def __init__ (self, current_Mobs, X=40, Y=48, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        self.upGoAnimation = Animation(["res\\hero1z.png","res\\hero2z.png","res\\hero3z.png","res\\hero4z.png"],100)
        self.downGoAnimation = Animation(["res\\herou1.png","res\\herou2.png","res\\herou3.png","res\\herou4.png"],100)
        self.rightGoAnimation = Animation(["res\\herol1.png","res\\herol2.png","res\\herol3.png","res\\herol4.png"],100)
        self.leftGoAnimation = Animation(["res\\herol1.png","res\\herol2.png","res\\herol3.png","res\\herol4.png"],100, True)
        self.leftAtackAnimation = Animation(["res\\PatackL.png","res\\PAL2.png","res\\PAL3.png","res\\PAL4.png"],100, True, shot_animation = True)
        self.rightAtackAnimation = Animation(["res\\PatackL.png","res\\PAL2.png","res\\PAL3.png","res\\PAL4.png"],100, shot_animation = True)

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
        self.current_Mobs = current_Mobs
        self.mov_module = MovingModule()
        self.is_game_pause = False
        self.contact_rect = pygame.Rect((self.x+8, self.y+8), (12, 12))

    def StopMoving(self):
        self.currentAnimation.Stop()
        self.mov_module.move_stop()

    def update(self, Walls, cameraPositionX, cameraPositionY):
        self.global_position_x = cameraPositionX+ int(self.x)
        self.global_position_y = cameraPositionY+ int(self.y)
        self.x, self.y = self.mov_module.update(self.x, self.y, self, Walls)
        self.image = self.currentAnimation.getImg()
        self.rect.topleft = (int(self.x), int(self.y))
        self.contact_rect.topleft = (int(self.x+8), int(self.y+8))
    def pause (self):
        self.is_game_pause = True
        self.mov_module.pause()
    
    def play (self):
        self.is_game_pause = False
        self.mov_module.run()

    def LeftAtack(self):
        if self.is_game_pause:
            return
        self.currentAnimation = self.leftAtackAnimation
        self.currentAnimation.Start()
        ans = pygame.sprite.spritecollideany(self,self.current_Mobs) 
        if not (ans is None):
            print("damage")
            ans.GetDamage("Left")

    def RightAtack(self):
        if self.is_game_pause:
            return
        self.currentAnimation = self.rightAtackAnimation
        self.currentAnimation.Start()
        ans = pygame.sprite.spritecollideany(self,self.current_Mobs) 
        if not (ans is None):
            print("damage")
            ans.GetDamage("Right")

    def _SetUpMoving(self, animation, speed, direction):
        if self.currentAnimation != animation:
            print("Wrong")
            self.currentAnimation =  animation
            self.currentAnimation.Start()
            if (direction == "x"):
                self.x_speed = speed
            else:
                self.y_speed = speed
        elif(self.currentAnimation == animation) and (not self.currentAnimation.isPlay):
            print("Start")
            self.currentAnimation.Start()
            if (direction == "x"):
                self.x_speed = speed
            else:
                self.y_speed = speed

    def MoveLeft (self):
        if self.is_game_pause:
            return
        self._SetUpMoving(self.leftGoAnimation, -0.1, "x")
        self.mov_module.move_left()

    def MoveRight (self):
        if self.is_game_pause:
            return
        self._SetUpMoving(self.rightGoAnimation, 0.1, "x")
        self.mov_module.move_right()

    def MoveUp (self):
        if self.is_game_pause:
            return
        self._SetUpMoving(self.upGoAnimation, -0.1, "y")
        self.mov_module.move_up()  

    def MoveDown (self):
        if self.is_game_pause:
            return
        self._SetUpMoving(self.downGoAnimation, 0.1, "y")
        self.mov_module.move_down()

    def GetDamage(self, direction):
        if self.is_game_pause:
            return
        import random 
        random.seed()
        shifting = random.randint(1, 16)
        self.time_object.add(TimeObjects.FromHeroText("-1", x = self.rect.x + shifting, y =self.rect.y - shifting))
        if len (pygame.sprite.spritecollide(self,self.Walls,False)) == 0:
            if direction == "Left":
                self.global_position_x = self.global_position_x - 5
            elif direction == "Right":
                self.global_position_x = self.global_position_x + 5

class Mob (pygame.sprite.Sprite):
    def __init__ (self, x_start_global, y_start_global, Walls, current_Mobs, time_object, cameraPositionX = 0, cameraPositionY = 0):
        pygame.sprite.Sprite.__init__(self)
        self.time_object = time_object
        self.upGoAnimation = Animation(["res\\hero1z.png","res\\hero2z.png","res\\hero3z.png","res\\hero4z.png"],100)
        self.downGoAnimation = Animation(["res\\herou1.png","res\\herou2.png","res\\herou3.png","res\\herou4.png"],100)
        self.rightGoAnimation = Animation(["res\\herol1.png","res\\herol2.png","res\\herol3.png","res\\herol4.png"],100)
        self.leftGoAnimation = Animation(["res\\herol1.png","res\\herol2.png","res\\herol3.png","res\\herol4.png"],100, True)
        self.leftAtackAnimation = Animation(["res\\PatackL.png","res\\PAL2.png","res\\PAL3.png","res\\PAL4.png"],100, True)
        self.rightAtackAnimation = Animation(["res\\PatackL.png","res\\PAL2.png","res\\PAL3.png","res\\PAL4.png"],100)
        self.currentAnimation = self.downGoAnimation
        self.image = self.currentAnimation.getImg()
        self.rect = self.image.get_rect(center=(0,0))
        self.isVisable = False
        self.Walls = Walls
        self.current_Mobs = current_Mobs
        self.x_speed = 0
        self.y_speed = 0
        self.x:float = 0
        self.y:float = 0
        self.privUpdateTime = 0
        self.state = None
        self.global_position_x = x_start_global
        self.global_position_y = y_start_global
        self.mov_module = MovingModule()

    def StopMoving(self):
        self.currentAnimation.Stop()
        self.x_speed = 0
        self.y_speed = 0
        self.mov_module.move_stop()                                                             
    def GetDamage(self, direction):
        import random 
        random.seed()
        shifting = random.randint(1, 16)
        self.time_object.add(TimeObjects.FromHeroText("-1", x = self.rect.x + shifting, y =self.rect.y - shifting, color = (0, 0, 255)))
        if len (pygame.sprite.spritecollide(self,self.Walls,False)) == 0:
            if direction == "Left":
                self.global_position_x = self.global_position_x - 5
            elif direction == "Right":
                self.global_position_x = self.global_position_x + 5

    def update(self, Walls, player, cameraPositionX, cameraPositionY, size):
        width, height = size
        self.player = player

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
            self.kill()
            return -1 
        else:
            self.current_Mobs.add(self)

        self.x = self.global_position_x - cameraPositionX*16
        self.y = self.global_position_y - cameraPositionY*16
        
        next_state = self.Intelect()
        if ((self.state is None) or (self.state != next_state)):
            print("Mob")
            self.state = next_state
            self.state()
        # dt = pygame.time.get_ticks() - self.privUpdateTime
        # self.privUpdateTime = pygame.time.get_ticks()
        # ### TODO need adding logic for analyze watsprite coliding
        # if (len (pygame.sprite.spritecollide(self,self.Walls,False)) > 0): # add mobs
        #     if self.x_speed > 0:
        #         self.x -= 5
        #     elif self.x_speed < 0:
        #         self.x += 5
        #     if self.y_speed > 0:
        #         self.y -= 5
        #     elif self.y_speed < 0:
        #         self.y += 5
        #     self.StopMoving()
        # else:
        #     self.x += dt*self.x_speed
        #     self.y += dt*self.y_speed
        self.x, self.y = self.mov_module.update(self.x, self.y, self, Walls)
        self.image = self.currentAnimation.getImg()
        self.rect.x = self.x
        self.rect.y = self.y
        #self.x, self.y = self.mov_module.update(self.x, self.y, self, Walls)
        self.global_position_x = cameraPositionX*16+ self.x
        self.global_position_y = cameraPositionY*16+ self.y 
        return True 

    def _SetUpMoving(self, animation, speed, direction):
        if self.currentAnimation != animation:
            print("Wrong")
            self.currentAnimation =  animation
            self.currentAnimation.Start()
            if (direction == "x"):
                self.x_speed = speed
            else:
                self.y_speed = speed
        elif(self.currentAnimation == animation) and (not self.currentAnimation.isPlay):
            print("Start")
            self.currentAnimation.Start()
            if (direction == "x"):
                self.x_speed = speed
            else:
                self.y_speed = speed

    def MoveLeft (self):
        self._SetUpMoving(self.leftGoAnimation, -0.1, "x")
        self.mov_module.move_left()

    def MoveRight (self):
        self._SetUpMoving(self.rightGoAnimation, 0.1, "x")
        self.mov_module.move_right()

    def MoveUp (self):
        self._SetUpMoving(self.upGoAnimation, -0.1, "y")
        self.mov_module.move_up()  

    def MoveDown (self):
        self._SetUpMoving(self.downGoAnimation, 0.1, "y")
        self.mov_module.move_down()

    def LeftAtack(self):
        self.currentAnimation = self.leftAtackAnimation
        self.currentAnimation.Start()
        ans = pygame.sprite.spritecollide(self,self.player) 
        #print(ans)
        if not (ans is None):
            print("damage")
            ans.GetDamage("Left")

    def RightAtack(self):
        self.currentAnimation = self.rightAtackAnimation
        self.currentAnimation.Start()
        #change option for mob 
        ans = pygame.sprite.spritecollideany(self,self.player) 
        #print(ans)
        if not (ans is None):
            print("damage")
            ans.GetDamage("Right")
        
    def Intelect (self): #return NextState
        if ((self.player.x - self.y >= -16) and (self.player.x - self.y <= 0)):
            return self.LeftAtack
        if (self.player.x - self.x > 16):
            return self.MoveRight
        elif (self.player.x - self.x < -16):
            return self.MoveLeft
        elif (self.player.x - self.y > 16):
            return self.MoveDown
        elif (self.player.x - self.y < -16):
            return self.MoveUp
        else:
            return self.StopMoving
        
class MovingModule:
    def __init__(self):
        self.fps = 60
        self.v_x = 0
        self.v_y = 0
        self.a_x = 0
        self.a_y = 0
        self.m = 0
        self.p_x = 0
        self.p_y = 0
        self.priv_t = pygame.time.get_ticks()
        self.__is_pause = False
    def move_left(self):
        self.v_x = -0.1
    def move_right(self):
        self.v_x = 0.1
    def move_up(self):
        self.v_y = -0.1
    def move_down(self):
        self.v_y = 0.1
    def move_stop(self):
        self.v_x = 0
        self.v_y = 0 
    def pause(self):
        self.__is_pause = True
    def run(self):
        self.__is_pause = False
    

    def update(self, x, y, sprite, walls):
        current = pygame.time.get_ticks() 
        dt = current - self.priv_t
        #print(dt) # problem dt increase 

        if (dt < 10):
            return x, y

        self.priv_t = current

        if self.__is_pause:
            return x, y

        collided_object = pygame.sprite.spritecollideany(sprite, walls)
        # added recursion for checking all collided object 

        if collided_object is not None:
            obj = collided_object
            dx = int(x)-obj.rect.x
            dy = int(y)-obj.rect.y
 
            # print("colide {} {}".format(dx, dy))
            sheeft_x = math.copysign((16 - math.fabs(dx)), dx)
            sheeft_y = math.copysign((16 - math.fabs(dy)), dy)
            if (self.v_x != 0):
                x = x + sheeft_x
            if (self.v_y != 0):
                y = y + sheeft_y
            self.v_x = 0
            self.v_y = 0
        x += dt*self.v_x
        y += dt*self.v_y
        self.p_x = x
        self.p_y = y 
        return x, y      




        


        

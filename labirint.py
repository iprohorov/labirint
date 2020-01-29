
import pygame
import labirint_gen
from player import Player
from player import Mob

class Wall (pygame.sprite.Sprite): 
    def __init__ (self, X=0, Y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.rect = self.image.get_rect(center=(X,Y))
    def clear_callback(surf, rect):
        color = 0, 0, 0
        surf.fill(color, rect)
       
class Camera :
    def __init__(self, size, xSize, ySize):
        self.size = size

        # Location size in Block
        self.xSize = xSize
        self.ySize = ySize
    
        self.cameraShiftX = int((width/16)/2)
        self.cameraShiftY = int((height/16)/2)
        
        self.cameraPositionX = 0
        self.cameraPositionY = 0

        self.privCameraPositionX = 0
        self.privCameraPositionY = 0

    def GetCameraShiftY(self, direction):
        defaultShift = int((height/16)/2) - 1 # number cels of shifting camera # need update for normal camera
        if  direction == "Down":
            print ("down")
            self.cameraShiftY = self.ySize - (self.cameraPositionY + defaultShift)
        else:
            print("UP work")
            self.cameraShiftY = self.cameraPositionY

        if self.cameraShiftY > defaultShift:
            self.cameraShiftY = defaultShift
            
    def GetCameraShiftX(self, direction):
        defaultShift = int((width/16)/2)
        if  direction == "Left":
            print("left")
            self.cameraShiftX = self.xSize - (self.cameraPositionX + int(width/16))
        else:
            print("rigt")
            self.cameraShiftX = self.cameraPositionX

        if self.cameraShiftX > defaultShift:
            self.cameraShiftX = defaultShift
    
    def handle_mod_position_left(self, mob):
        """ Return del mob or no
        """
        if (self.cameraPositionX <= int(mob.x)):
            print("Kill mob")
            mob.remove()
            return True
        else:
            mob.x -= self.cameraShiftX*16
            return False

    def handle_mod_position_right(self, mob):
        """ Return del mob or no
        """
        if (self.cameraPositionX <= width - int(mob.x)):
            print("Kill mob")
            mob.remove()
            return True
        else:
            mob.x -= self.cameraShiftX*16
            return False

    def handle_mod_position_up(self, mob):
        pass 

    def handle_mod_position_down(self, mob):
        pass

    def update_mobs_position(self, mobs_list, direction):
        if (mobs_list is None) or mobs_list == []:
            print ("no mobs")
            return None
        if direction == "Left":
            for mob in mobs_list:
                if self.handle_mod_position_left(mob):
                    mobs_list.remove(mob)
        if direction == "Right":
            for mob in mobs_list:
                if self.handle_mod_position_right(mob):
                    mobs_list.remove(mob)

    def update(self, player, mobs_list = None): # if croossing  position update camera
        
        shift_left_trashold = width-(16*4)  #when start scroling
        shift_right_trashold = 16*2
        shift_down_trashold = height-(16*4) 
        shift_up_trashold = 16*2

        if ((player.rect.x > shift_left_trashold) and  (self.xSize*16 - self.cameraPositionX*16 - width > 0)): 
            print("debug")
            self.GetCameraShiftX("Left") # error right ?
            self.privCameraPositionX = self.cameraPositionX
            self.cameraPositionX += self.cameraShiftX
            player.x -= self.cameraShiftX*16
            self.update_mobs_position(mobs_list,"Left")
            return True

        if ((player.rect.x < shift_right_trashold) and (self.cameraPositionX != 0)):
            self.GetCameraShiftX("Right")
            self.privCameraPositionX = self.cameraPositionX 
            self.cameraPositionX -= self.cameraShiftX
            player.x += self.cameraShiftX*16
            return True             

        if ((player.rect.y > shift_down_trashold) and  (self.ySize*16 - self.cameraPositionY*16 - height > 0)):
            self.GetCameraShiftY("Down")
            self.privCameraPositionY = self.cameraPositionY
            self.cameraPositionY += self.cameraShiftY
            player.y -= self.cameraShiftY*16
            return True

        if ((player.rect.y < shift_up_trashold) and (self.cameraPositionY != 0)):
            self.GetCameraShiftY("Up")
            self.privCameraPositionY = self.cameraPositionY
            self.cameraPositionY -= self.cameraShiftY
            player.y += self.cameraShiftY*16
            return True
        return False

        
        
#map.generate()

pygame.init()

#size = width, height = 1366, 768
size = width, height = 640, 480
titleSize = 16
speed = [2, 2]
backcolor = 71, 45, 60
#screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
location = labirint_gen.Labyrinth(5,5) #50 50
location.dbgPrint()
wallMap, locationSizeX, locationSizeY = location.draw()
camera = Camera(size, locationSizeX, locationSizeY)

cameraPositionX = 0
cameraPositionY = 0

privCameraPositionX = 0
privCameraPositionY = 0


Walls= pygame.sprite.Group()
player = Player()
current_mobs = [Mob(X=64, Y=64)]
light=pygame.image.load('light.png')



def DrawMAP (camera):
    # global cameraPositionX
    # global cameraPositionY

    # if(cameraPositionX < 0):
    #     cameraPositionX = 0

    # if(cameraPositionY < 0):
    #     cameraPositionY = 0

    # print (xSize,ySize)
    
    # Walls.clear(screen)
    Walls.empty()
    # print(Darw)
    # for row in wallMap:
    #     print (row)
    fullScreenSizeX = camera.cameraPositionX+int(width/16)+1 # number cells in x 
    fullScreenSizeY = camera.cameraPositionY+int(height/16)+1 # number cells in x 

    if (fullScreenSizeY>len(wallMap)):
        fullScreenSizeY = len(wallMap)
    if (fullScreenSizeX>len(wallMap[0])):
        fullScreenSizeX = len(wallMap[0])
    
        
    
    for x in range (camera.cameraPositionX,fullScreenSizeX):
        for y in range (camera.cameraPositionY,fullScreenSizeY):
            if (wallMap[y][x]):
                Walls.add(Wall((x-camera.cameraPositionX)*16,(y-camera.cameraPositionY)*16))


    return True

FLAG = True
isNeeedUpdateLocation = True
FirstRUN = True


while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.MoveLeft()
            if event.key == pygame.K_RIGHT:
                player.MoveRight()
            if event.key == pygame.K_DOWN:
                player.MoveDown()
            if event.key == pygame.K_UP:
                player.MoveUp()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.StopMoving()
            if event.key == pygame.K_RIGHT:
                player.StopMoving()
            if event.key == pygame.K_DOWN:
                player.StopMoving()
            if event.key == pygame.K_UP:
                player.StopMoving()

    isNeeedUpdateLocation = camera.update(player, current_mobs)
    if isNeeedUpdateLocation or FirstRUN:
        FirstRUN = False
        DrawMAP(camera)
    
    screen.fill(backcolor)    
    player.update(Walls)

    for mob in current_mobs:
        mob.update(Walls, player.x, player.y)
    
    
    
    Walls.draw(screen)
   
    screen.blit(player.image, player.rect)

    for mob in current_mobs:
        screen.blit(mob.image, mob.rect)

    filter = pygame.surface.Surface((width+100, height+100))
    filter.fill(pygame.color.Color('Grey'))
    filter.blit(light, (int(player.x), int(player.y)))
    screen.blit(filter, (-42, -42), special_flags=pygame.BLEND_RGBA_SUB)
    pygame.display.flip()
    #pygame.display.update()
            






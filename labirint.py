

import sys
import pygame
from random import randint
from player import Player
sys.setrecursionlimit(10000)

class Wall (pygame.sprite.Sprite): 
    def __init__ (self, X=0, Y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.rect = self.image.get_rect(center=(X,Y))
    def clear_callback(surf, rect):
        color = 0, 0, 0
        surf.fill(color, rect)


# labyrinth = [[Wall (X=x,Y=y) for x in range (10)] for y in range (10)]

# print  (labyrinth)
# for walls in labyrinth:
#     for wall in walls:
#         print (wall)
LABYRINTH_SIZE_X = 10
LABYRINTH_SIZE_Y = 10

class Room: 
    def __init__ (self, X=0, Y=0):
        self.wall = [True,True,True,True]
        self.x = X
        self.y = Y
        self.visit = False
    # def draw (self):
    #     sys.stdout.write("----\n\r")
    #     sys.stdout.write("|  |\n\r")
    #     sys.stdout.write("|  |\n\r")
    #     sys.stdout.write("----\n\r")
    def dell (self,wall):
        if (self.x == 0 and wall == 0):
            print("solid")
            return False
        if (self.y == 0 and wall == 1):
            print("solid")
            return False
        if (self.x ==  LABYRINTH_SIZE_X-1 and wall == 2):
            print("solid")
            return False
        if (self.y ==  LABYRINTH_SIZE_Y-1 and wall == 3):
            print("solid")
            return False
        self.wall[wall] = False
        return True
    def __str__ (self):
        return "Room {} {}, Visit{} Wall {} {} {} {}".format(self.x,self.y,self.visit, self.wall[0],self.wall[1],self.wall[2],self.wall[3])

class Labyrinth ():
    def __init__ (self,screen, sizeX,sizeY):
        self.labyrinth = [[Room (X=x,Y=y) for x in range (sizeY)] for y in range (sizeX)]
        self.route = [(0,0)]
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.generate()

    def generateIsCompleat (self):
        for row_rooms in self.labyrinth:
            for room in row_rooms:
                if room.visit == False: 
                    #print ("aaal")
                    return False
                    
        return True 
    
    def checkRoomVisit (self,x,y):
        count = 0
        if (x-1 < 0 or self.labyrinth[x-1][y].visit):
            count += 1

        if (x+1 > (self.sizeX-1)) or self.labyrinth[x+1][y].visit:
            count +=1

        if (y-1 < 0 or self.labyrinth[x][y-1].visit):
            count += 1

        if (y+1 > (self.sizeY-1)) or self.labyrinth[x][y+1].visit:
            count += 1
        #print (count)
        if count == 4:
            return (True)
        else:
            return (False)

    def dellWall (self,new_position):
        x,y = self.route[len(self.route)-1]
        self.labyrinth[x][y].wall[new_position[3]] = False
        if (new_position[3] == 0):
            self.labyrinth[new_position[1]][new_position[2]].wall[2] = False
        if (new_position[3] == 1):
            self.labyrinth[new_position[1]][new_position[2]].wall[3] = False
        if (new_position[3] == 2):
            self.labyrinth[new_position[1]][new_position[2]].wall[0] = False
        if (new_position[3] == 3):
            self.labyrinth[new_position[1]][new_position[2]].wall[1] = False


            


         

    def generate (self):
        while (True):
            x,y =  self.route[len(self.route)-1]
            self.labyrinth[x][y].visit = True
            new_position = self.selectNextPosition (x,y) # res,x,y,dir
            #print(self.route)
            if new_position[0]:
                #input()
                if not self.generateIsCompleat():
                    if (self.labyrinth[new_position[1]][new_position[2]].visit == False) and (self.checkRoomVisit(x,y) == False):
                        #print ("next step")
                        self.dellWall(new_position)
                        self.route.append((new_position[1],new_position[2]))
                        self.debug()
                        #self.draw()
                        continue #self.generate()
                    elif self.checkRoomVisit(x,y):
                        #print ("next priv")
                        self.route.pop()
                        continue #self.generate()
                    elif self.labyrinth[new_position[1]][new_position[2]].visit :
                        continue #self.generate()
                else:
                    print ("visiting end")
                    #self.draw()
                    return True
            else:
                #print ("visiting")
                return self.generate()
    def selectNextPosition (self, x, y):
        direction = randint(0,3)
        #print ("dir {} ".format(direction))

        if (direction == 0) and (x != 0):
            x -= 1
            return (True,x,y,direction)
        if (direction == 2) and (x != self.sizeX-1):
            x += 1
            return (True,x,y,direction)
        if (direction == 1) and ( y != 0):
            y -= 1
            return (True,x,y,direction)
        if (direction == 3) and (y != self.sizeY-1):
            y += 1
            return (True,x,y,direction)
        

        return (False ,x,y,direction)
        
    def debug (self):
        pass
        # for rooms_row in self.labyrinth:
        #     for room in rooms_row:
        #         print(room)
    def dbgPrint (self):
        for x in range (self.sizeY):
            lines = ["", "", ""]
            for y in range (self.sizeX):
                if self.labyrinth[y][x].wall[1]:
                    lines[0] += "***"
                else:
                    lines[0] += "* *"

                if self.labyrinth[y][x].wall[3]:
                    lines[2] += "***"
                else:
                    lines[2] += "* *"

                if self.labyrinth[y][x].wall[0]:
                    lines[1] += "| "
                else:
                    lines[1] += "  "
                if self.labyrinth[y][x].wall[2]:
                    lines[1] += "|"
                else:
                    lines[1] += " "
            for line in lines:
                sys.stdout.write(line+"\r\n")


    def _drawDownwall (self, x, y):
        for i in range (self.scaleX):
            self.wallMap[x*self.scaleY+(self.scaleY-1)][y*self.scaleX+i] = 1
    
    def _drawUpwall (self, x, y):
        for i in range (self.scaleX):
            self.wallMap[x*self.scaleY][y*self.scaleX+i] = 1
    
    def _drawLeftwall (self, x, y):
        for i in range (self.scaleY):
            self.wallMap[x*self.scaleY+i][y*self.scaleX] = 1
    
    def _drawRightwall (self, x, y):
        for i in range (self.scaleY):
            self.wallMap[x*self.scaleY+i][y*self.scaleX + (self.scaleX-1)] = 1
    


    def draw (self):
        self.scaleX = 8
        self.scaleY = 8
        self.wallMap = [[ 0 for x in range(self.sizeX*self.scaleY)] for y in range(self.sizeY*self.scaleX)]
        #print (wallMap) # 3 cells 

        for x in range (self.sizeY): # y == x normal
            for y in range (self.sizeX):
                if x == 0:
                    self._drawUpwall(x,y)
                    if self.labyrinth[y][x].wall[3]:
                        self._drawDownwall(x,y)
                elif x == self.sizeX-1:
                    self._drawDownwall(x,y)
                else:
                    if self.labyrinth[y][x].wall[3]:
                        self._drawDownwall(x,y)
                if y == 0:
                    self._drawLeftwall(x,y)
                    if self.labyrinth[y][x].wall[2]:
                        self._drawRightwall(x,y)
                elif y == self.sizeY-1:
                    self._drawRightwall(x,y)
                else:
                    if self.labyrinth[y][x].wall[2]:
                        self._drawRightwall(x,y)
        return (self.wallMap.copy(), self.sizeX*self.scaleX, self.sizeY*self.scaleY) # first y second Y

        # for row in wallMap:
        #     print (row)
        # for x in range (self.sizeX*scaleX):
        #     for y in range (self.sizeY*scaleY):
        #         if (wallMap[y][x]):
        #             pygame.draw.rect(screen, (255, 255, 255), (x*10, y*10, 10, 10))

        # pygame.display.update()


class Camera :
    def __init__(self, size):
        self.size = size

        width, height = size
        
        self.cameraShiftX = int((width/16)/2)
        self.cameraShiftY = int((height/16)/2)
        
        self.cameraPositionX = 0
        self.cameraPositionY = 0

        self.privCameraPositionX = 0
        self.privCameraPositionY = 0

    def GetCameraShiftY(self, direction):
        defaultShift = int((height/16)/2) - 1 # number cels of shifting camera
        if  direction == "Down":
            print ("down")
            self.cameraShiftY = ySize - (self.cameraPositionY + defaultShift)
        else:
            print("UP work")
            self.cameraShiftY = self.cameraPositionY

        if self.cameraShiftY > defaultShift:
            self.cameraShiftY = defaultShift
            
    def GetCameraShiftX(self, direction):
        defaultShift = int((width/16)/2) - 1
        if  direction == "Left":
            print("left")
            self.cameraShiftX = xSize - (self.cameraPositionX + defaultShift)
        else:
            print("rigt")
            self.cameraShiftX = self.cameraPositionX

        if self.cameraShiftX > defaultShift:
            self.cameraShiftX = defaultShift
            
               
    def update(self, player, xSize, ySize): # if croossing  position update camera
        self.cameraShiftX = int((width/16)/2)
        self.cameraShiftY = int((height/16)/2)
        x_speed = player.x_speed
        y_speed = player.y_speed
        #player.StopMoving()
        

        #print ("y: {} {}".format(self.cameraShiftY, self.cameraPositionY ))
        
        if ((player.rect.x > 16*self.cameraShiftX)):    #depends in screen size # add(cameraPositionX+int(width/16)+1) > xSize
            print("debug")
            self.GetCameraShiftX("Left")
            self.privCameraPositionX = self.cameraPositionX
            self.cameraPositionX += self.cameraShiftX
            player.x -= self.cameraShiftX*16
            return True

        if ((player.rect.x < 16) and (self.cameraPositionX != 0)):
            self.GetCameraShiftX("Right")
            self.privCameraPositionX = self.cameraPositionX 
            self.cameraPositionX -= self.cameraShiftX
            player.x += self.cameraShiftX*16
            return True             

        if ((player.rect.y > 16*self.cameraShiftY) ):
            self.GetCameraShiftY("Down")
            self.privCameraPositionY = self.cameraPositionY
            self.cameraPositionY += self.cameraShiftY
            player.y -= self.cameraShiftY*16
            return True

        if ((player.rect.y < 16) and (self.cameraPositionY != 0)):
            self.GetCameraShiftY("Up")
            self.privCameraPositionY = self.cameraPositionY
            self.cameraPositionY -= self.cameraShiftY
            player.y += self.cameraShiftY*16
            return True

        if (camera.cameraPositionX+int(width/16)+1) > xSize: # xSize full labirinth size in block 
            pass
            #print ("X end")
            #camera.cameraPositionX = camera.privCameraPositionX
            #player.rect.x = privPlayerX

        if (camera.cameraPositionY+int(height/16)+1) > ySize:
            pass
            #print ("Y end")
            #camera.cameraPositionY = camera.privCameraPositionY
            #player.rect.y = privPlayerY
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
map = Labyrinth(screen,2,2) #50 50
map.dbgPrint()
wallMap, xSize, ySize = map.draw()
camera = Camera(size)
cameraPositionX = 0
cameraPositionY = 0

privCameraPositionX = 0
privCameraPositionY = 0


Walls= pygame.sprite.Group()
player = Player()



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
                # print (x,y)
                Walls.add(Wall((x-camera.cameraPositionX)*16,(y-camera.cameraPositionY)*16))


    return True

FLAG = True
isNeeedUpdateLocation = True
FirstRUN = True
while 1:
    #event 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.MoveLeft()
                #cameraPositionX += 1
            if event.key == pygame.K_RIGHT:
                player.MoveRight()
                #cameraPositionX -= 1
            if event.key == pygame.K_DOWN:
                player.MoveDown()
                #cameraPositionY -= 1
            if event.key == pygame.K_UP:
                player.MoveUp()
                #cameraPositionY += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.StopMoving()
                #cameraPositionX += 1
            if event.key == pygame.K_RIGHT:
                player.StopMoving()
                #cameraPositionX -= 1
            if event.key == pygame.K_DOWN:
                player.StopMoving()
                #cameraPositionY -= 1
            if event.key == pygame.K_UP:
                player.StopMoving()
                #cameraPositionY += 1
    #drawing
    
    
    
    
    
    isNeeedUpdateLocation = camera.update(player, xSize, ySize)
    
    if isNeeedUpdateLocation or FirstRUN:
        FirstRUN = False
        DrawMAP(camera)
    
    screen.fill(backcolor)    
    player.update(Walls)
    
    
    
    Walls.draw(screen)
   
    screen.blit(player.image, player.rect)
    pygame.display.update()
            






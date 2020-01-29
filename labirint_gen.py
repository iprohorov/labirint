import sys
from random import randint
LABYRINTH_SIZE_X = 10
LABYRINTH_SIZE_Y = 10

class Room: 
    def __init__ (self, X=0, Y=0):
        self.wall = [True,True,True,True]
        self.x = X
        self.y = Y
        self.visit = False
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
    def __init__ (self, sizeX, sizeY):
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
                        #self.debug()
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
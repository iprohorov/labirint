
import pygame
import labirint_gen
import TimeObjects
import pytmx
from player import Player
from player import Mob


class Wall (pygame.sprite.Sprite): 
    def __init__ (self, X=0, Y=0, image = None):
        pygame.sprite.Sprite.__init__(self)
        if (image is None):
            self.image = pygame.image.load("wall.png").convert_alpha()
        else:
            self.image = image
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
        
        self.width = Game.screen_setting["size"][0]
        self.height = Game.screen_setting["size"][1]

        self.cameraShiftX = int((self.width/16)/2)
        self.cameraShiftY = int((self.height/16)/2)
        
        self.cameraPositionX = 0
        self.cameraPositionY = 0

        self.privCameraPositionX = 0
        self.privCameraPositionY = 0

        self.privShiftDerection = None

    def GetCameraShiftY(self, direction):
        defaultShift = int((self.height/16)/2) - 1 # number cels of shifting camera # need update for normal camera
        if  direction == "Down":
            print ("down")
            self.cameraShiftY = self.ySize - (self.cameraPositionY + defaultShift)
        else:
            print("UP work")
            self.cameraShiftY = self.cameraPositionY

        if self.cameraShiftY > defaultShift:
            self.cameraShiftY = defaultShift
            
    def GetCameraShiftX(self, direction):
        defaultShift = int((self.width/16)/2)
        if  direction == "Left":
            print("left")
            self.cameraShiftX = self.xSize - (self.cameraPositionX + int(self.width/16))
        else:
            print("rigt")
            self.cameraShiftX = self.cameraPositionX

        if self.cameraShiftX > defaultShift:
            self.cameraShiftX = defaultShift

    def update(self, player): # if croossing  position update camera
        
        shift_left_trashold = self.width-(16*4)  #when start scroling
        shift_right_trashold = 16*2
        shift_down_trashold = self.height-(16*4) 
        shift_up_trashold = 16*2

        if ((player.rect.x > shift_left_trashold) and  (self.xSize*16 - self.cameraPositionX*16 - self.width > 0)): 
            print("debug")
            self.GetCameraShiftX("Left") # error right ?
            self.privCameraPositionX = self.cameraPositionX
            self.cameraPositionX += self.cameraShiftX
            player.x -= self.cameraShiftX*16
            self.privShiftDerection = "Left"
            return True

        if ((player.rect.x < shift_right_trashold) and (self.cameraPositionX != 0)):
            self.GetCameraShiftX("Right")
            self.privCameraPositionX = self.cameraPositionX 
            self.cameraPositionX -= self.cameraShiftX
            player.x += self.cameraShiftX*16
            self.privShiftDerection = "Right"
            return True             

        if ((player.rect.y > shift_down_trashold) and  (self.ySize*16 - self.cameraPositionY*16 - self.height > 0)):
            self.GetCameraShiftY("Down")
            self.privShiftDerection = "Down"
            self.privCameraPositionY = self.cameraPositionY
            self.cameraPositionY += self.cameraShiftY
            player.y -= self.cameraShiftY*16
            return True

        if ((player.rect.y < shift_up_trashold) and (self.cameraPositionY != 0)):
            self.GetCameraShiftY("Up")
            self.privShiftDerection = "Up"
            self.privCameraPositionY = self.cameraPositionY
            self.cameraPositionY -= self.cameraShiftY
            player.y += self.cameraShiftY*16
            return True
        return False



class Game:
    screen_setting = {"size":(1366, 768), "backcolor": (71, 45, 60), "light":False}
    status = {""}
    walls = None
    current_mobs = None 
    time_object = None
    game_map = None
    locationSizeX = None
    locationSizeY = None
    location_pieces = None
    def __init__ (self):
        #group consist static solid object
        Game.walls = pygame.sprite.Group()
        #display mobs using for colide detected 
        Game.current_mobs = pygame.sprite.Group()
        #group for showing time object 
        Game.time_object = pygame.sprite.Group()
        #generate map
        location = labirint_gen.Labyrinth(50,50)
        location.dbgPrint()
        #load tmx map for room
        Game.location_pieces = self.load_location_piece()
        Game.game_map, Game.locationSizeX, Game.locationSizeY = location.drawUseTMX(Game.location_pieces)
        print(f"MAP:{Game.locationSizeX},{Game.locationSizeY}")
    def load_location_piece(self):
        location_pieces = {0:pytmx.load_pygame('image\\Tilemap\\t0.tmx'), 
                           1:pytmx.load_pygame('image\\Tilemap\\t1.tmx'),
                           2:pytmx.load_pygame('image\\Tilemap\\t2.tmx')}
        return location_pieces

def DrawMAP (camera):
    # clean map 
    Game.walls.empty()
    width, height = Game.screen_setting["size"]


    fullScreenSizeX = camera.cameraPositionX+int(width/16)+1 # number cells in x 
    fullScreenSizeY = camera.cameraPositionY+int(height/16)+1 # number cells in x 

    if (fullScreenSizeY>len(Game.game_map)):
        fullScreenSizeY = len(Game.game_map)
    if (fullScreenSizeX>len(Game.game_map[0])):
        fullScreenSizeX = len(Game.game_map[0])
    
    for x in range (camera.cameraPositionX,fullScreenSizeX):
        for y in range (camera.cameraPositionY,fullScreenSizeY):
            #Wals is static object 
            if (not(Game.game_map[y][x] is None)):
                 Game.walls.add(Wall((x-camera.cameraPositionX)*16,(y-camera.cameraPositionY)*16,image = Game.location_pieces[Game.game_map[y][x][0]].get_tile_image_by_gid(Game.game_map[y][x][1])))
    return True

def main ():
    pygame.init()
    screen = pygame.display.set_mode(Game.screen_setting["size"])
    game = Game()
    camera = Camera(Game.screen_setting["size"], Game.locationSizeX, Game.locationSizeY)
    player = Player(Game.current_mobs)
    # list of mobs contaned all living mobs in game 
    all_mobs_list = [Mob(64+x*16, 64+16*x, Game.walls, Game.current_mobs, Game.time_object) for x in range(1)]
    #append current mob for colide detection in current camera position
    for mob in all_mobs_list:
        Game.current_mobs.add(mob)

    light=pygame.image.load('light.png')

    pygame.font.init()
    myfont = pygame.font.SysFont('Aria', 24)


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
                if event.key == pygame.K_a:
                    player.LeftAtack()
                if event.key == pygame.K_d:
                    player.RightAtack()

        isNeeedUpdateLocation = camera.update(player) 
        if isNeeedUpdateLocation or FirstRUN:
            FirstRUN = False
            DrawMAP(camera)
        
        screen.fill(Game.screen_setting["backcolor"])    
        player.update(Game.walls, camera.cameraPositionX, camera.cameraPositionY)

        for mob in all_mobs_list:
            mob.update(player, camera.cameraPositionX, camera.cameraPositionY, Game.screen_setting["size"])
        
        
        Game.walls.draw(screen)
        Game.time_object.draw(screen)
        Game.time_object.update()
        screen.blit(player.image, player.rect)

        for mob in all_mobs_list:
            if mob.isVisable:
                screen.blit(mob.image, mob.rect)
        
        if Game.screen_setting["light"]:
            filter = pygame.surface.Surface((width+100, height+100))
            filter.fill(pygame.color.Color('Grey'))
            filter.blit(light, (int(player.x), int(player.y)))
            screen.blit(filter, (-42, -42), special_flags=pygame.BLEND_RGBA_SUB)

        textsurface = myfont.render("Cam {}, {} Mob: {},{} ".format(camera.cameraPositionX, camera.cameraPositionY, int(all_mobs_list[0].global_position_x), int(all_mobs_list[0].global_position_y)), False, (255, 0, 0))
        screen.blit(textsurface,(0,0))
        pygame.display.flip()
        #pygame.display.update()

if __name__== "__main__":
  main()
            
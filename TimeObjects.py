import pygame
class FromHeroText (pygame.sprite.Sprite):
#This text generate mobs or player. This text have live time.
    def __init__ (self, str, x = 0, y = 0, life_time = 1000):
        pygame.sprite.Sprite.__init__(self)
        self.life_time = life_time
        self.createTime = pygame.time.get_ticks()
        myfont = pygame.font.SysFont('Aria', 24)
        self.image = myfont.render("str", False, (255, 0, 0))
        self.rect = self.image.get_rect(center=(x,y))
    def update(self):
        if self.createTime + self.life_time < pygame.time.get_ticks():
            self.kill()
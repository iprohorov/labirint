import pygame


class FromHeroText (pygame.sprite.Sprite):
#This text generate mobs or player. This text have live time.
    def __init__ (self, text, x = 0, y = 0, life_time = 400, color = (255, 0, 0)):
        #TODO add animation and transparency
        pygame.sprite.Sprite.__init__(self)
        self.life_time = life_time
        self.createTime = pygame.time.get_ticks()
        myfont = pygame.font.SysFont('Aria', 24)
        self.image = myfont.render(text, False, color)
        self.rect = self.image.get_rect(center=(x,y))
        self.alfa = 255
        self.alfa_time = self.createTime
        self.alfa_dt = 240//(life_time//10)
    def update(self):
        
        if (self.alfa_time+self.life_time/10) < pygame.time.get_ticks():
             self.alfa = self.alfa - self.alfa_dt

        self.image.set_alpha(self.alfa)
        if self.createTime + self.life_time < pygame.time.get_ticks():
            self.kill()
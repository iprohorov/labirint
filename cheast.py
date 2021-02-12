import pygame
import random
import TimeObjects

class Chest (pygame.sprite.Sprite):
    """We can use only location. Use image loadings from file for open or close cheats"""
    def __init__ (self, X, Y, image, time_object):
        pygame.sprite.Sprite.__init__(self)
        self.time_object = time_object
        self.image = image
        self.rect = self.image.get_rect(center=(X,Y))
        self.last_open_time = 0
    def clear_callback(surf, rect):
        color = 0, 0, 0
        surf.fill(color, rect)
    def do (self):
        if pygame.time.get_ticks() - self.last_open_time < 1000:
            return 

        shifting = random.randint(1, 16)
        self.time_object.add(TimeObjects.FromHeroText("Oh empty!", x = self.rect.x + shifting, y =self.rect.y - shifting, color = (128, 128, 128), life_time = 600))
        self.last_open_time = pygame.time.get_ticks()
    def check_colide (self, player_rect, action):
        ans = self.rect.colliderect(player_rect)
        if ans and action:
            self.do()
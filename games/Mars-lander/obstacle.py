import pygame
import random


class Obstacle(pygame.sprite.Sprite):
    def __init__(a2, x, y):
        obstacles_list = [
            'building_dome',
            'building_station_NE',
            'building_station_SW',
            'pipe_ramp_NE',
            'pipe_stand_SE',
            'rocks_NW',
            'rocks_ore_SW',
            'rocks_small_SE',
            'satellite_SE',
            'satellite_SW'
        ]
        pygame.sprite.Sprite.__init__(a2)
        a2.image = pygame.image.load('resources/obstacles/' + random.choice(obstacles_list) + '.png')
        a2.rect = a2.image.get_rect()
        a2.rect.center = (x, y)

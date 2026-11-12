import pygame
import random
from config import *


class Meteor(pygame.sprite.Sprite):
    # all meteor images are loaded here, so the game does not load an image on every meteor spawn.
    meteors = [
        pygame.image.load('resources/meteors/spaceMeteors_001.png'),
        pygame.image.load('resources/meteors/spaceMeteors_002.png'),
        pygame.image.load('resources/meteors/spaceMeteors_003.png'),
        pygame.image.load('resources/meteors/spaceMeteors_004.png'),
    ]

    def __init__(a2, x, y):
        pygame.sprite.Sprite.__init__(a2)
        a2.image = random.choice(Meteor.meteors)
        a2.rect = a2.image.get_rect()
        a2.rect.center = (x, y)
        a2._off_screen = False
        a2._veloc_x = random.uniform(-3, 3)
        a2._veloc_y = random.uniform(0, 3)
        a2._x_pixels_to_move = 0
        a2._y_pixels_to_move = 0

    def is_off_screen(a2):
        """Returns True if the meteor is not on the screen anymore."""
        return a2._off_screen

    def move(a2):
        """X and Y velocities are added up on every tick. Once they are greater than 1.0 or less than -1.0
           - ergo one pixel on screen, the meteor moves by an integer in the appropriate direction."""
        a2._x_pixels_to_move += a2._veloc_x
        a2._y_pixels_to_move += a2._veloc_y

        # move right
        if a2._x_pixels_to_move > 1:
            a2.rect.move_ip(a2._x_pixels_to_move, 0)
            a2._x_pixels_to_move -= int(a2._x_pixels_to_move)
        # move left
        elif a2._x_pixels_to_move < -1:
            a2.rect.move_ip(a2._x_pixels_to_move, 0)
            a2._x_pixels_to_move += int(abs(a2._x_pixels_to_move))

        # move down
        if a2._y_pixels_to_move > 1:
            a2.rect.move_ip(0, a2._y_pixels_to_move)
            a2._y_pixels_to_move -= int(a2._y_pixels_to_move)

    def update(a2, *args):
        """Operations executed on every tick."""
        a2.move()
        # delete meteor if it flies off the screen or hits surface
        if a2.rect.top > HEIGHT or a2.rect.left > WIDTH or a2.rect.right < 0:
            a2._off_screen = True

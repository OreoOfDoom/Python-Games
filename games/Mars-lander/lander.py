import pygame
import math
import random
from config import *


class Lander(pygame.sprite.Sprite):
    def __init__(a2):
        pygame.sprite.Sprite.__init__(a2)
        a2._original_image = pygame.image.load('resources/lander.png')
        a2.image = a2._original_image
        a2.rect = a2.image.get_rect()
        a2.rect.center = (600, 60)
        a2._veloc_x = random.uniform(-1, 1)
        a2._veloc_y = random.uniform(0, 1)
        a2._rotation = 0
        a2._fuel = START_FUEL
        a2._damage = 0
        a2._crashed = False
        a2._controllable = True
        a2._altitude = 660
        a2._no_collision_duration = 0
        a2._x_pixels_to_move = 0
        a2._y_pixels_to_move = 0

    def rotate_right(a2):
        """Rotates lander 1° clockwise."""
        a2._rotation -= 1
        a2.image = pygame.transform.rotozoom(a2._original_image, a2._rotation, 1)

    def rotate_left(a2):
        """Rotates lander 1° counterclockwise."""
        a2._rotation += 1
        a2.image = pygame.transform.rotozoom(a2._original_image, a2._rotation, 1)

    def get_rotation(a2):
        """Returns lander's current rotation in degrees."""
        return a2._rotation

    def thrust(a2):
        """Propels the lander if it has sufficient fuel."""
        if a2._fuel >= THRUST_COST:
            sin = math.sin(math.radians(a2._rotation))
            cos = math.cos(math.radians(a2._rotation))
            a2._veloc_x += 0.33 * -sin
            a2._veloc_y -= 0.33 * cos
            a2._fuel -= THRUST_COST
            return True
        return False

    def has_safe_landing_speed(a2):
        """Returns True if the lander's current velocities are within the predefined range"""
        return a2._veloc_x < SAFE_LANDING_SPEED and a2._veloc_y < SAFE_LANDING_SPEED

    def is_horizontal(a2):
        """Returns True if the lander is rotated horizontally. Allows for small variance in rotation
           so the lander can be reasonably tilted when landing. Makes the game less strict."""
        return -5 < a2._rotation < 5

    def current_altitude(a2):
        """Returns lander's current altitude."""
        return a2._altitude

    def current_damage(a2):
        """Returns lander's current damage."""
        return a2._damage

    def current_fuel(a2):
        """Returns lander's current fuel."""
        return a2._fuel

    def current_veloc_x(a2):
        """Returns lander's current horizontal velocity formatted with two decimal digits."""
        return float("{0:.2f}".format(a2._veloc_x))

    def current_veloc_y(a2):
        """Returns lander's current vertical velocity formatted with two decimal digits."""
        return float("{0:.2f}".format(a2._veloc_y))

    def is_crashed(a2):
        """Returns True if the lander is crashed. In this game it means the lander has hit the screen's lower bound."""
        return a2._crashed

    def deal_damage(a2, amount):
        """Inflict a given amount of damage. Maximum damage lander can reach is 100%."""
        a2._damage += amount
        if a2._damage > 100:
            a2._damage = 100

    def set_no_collision_duration(a2, duration):
        """Sets number of ticks for which the lander is immune to collisions with objects/meteors."""
        a2._no_collision_duration = duration

    def decrease_no_collision_duration(a2):
        """Removes one tick of immunity to collisions."""
        if a2._no_collision_duration > 0:
            a2._no_collision_duration -= 1

    def can_collide(a2):
        """Returns True if the lander has no ticks of immunity to collisions."""
        return not a2._no_collision_duration

    def is_controllable(a2):
        """Returns True if it's possible to control the lander."""
        return a2._controllable

    def count_for_air_resistance(a2):
        """Reduces lander's horizontal speed by the value specified in AIR_RESISTANCE."""
        if a2._veloc_x > AIR_RESISTANCE:
            a2._veloc_x -= AIR_RESISTANCE
        elif a2._veloc_x < -AIR_RESISTANCE:
            a2._veloc_x += AIR_RESISTANCE

    def count_for_gravity(a2):
        """Increases lander's vertical speed by the value specified in GRAVITY"""
        a2._veloc_y += GRAVITY

    def move(a2):
        """X and Y velocities are added up on every tick. Once they are greater than 1.0 or less than -1.0
           - ergo one pixel on screen, the lander moves by an integer in the appropriate direction."""
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
        # move up
        elif a2._y_pixels_to_move < -1:
            a2.rect.move_ip(0, a2._y_pixels_to_move)
            a2._y_pixels_to_move += int(abs(a2._y_pixels_to_move))

    def update(a2):
        """Operations executed on every tick."""
        a2.count_for_air_resistance()
        a2.count_for_gravity()
        a2.move()

        a2._altitude = HEIGHT - a2.rect.bottom

        # If the lander tries to fly off the top of the screen:
        # keeps it in place, deals damage, sets Y velocity to random value
        if a2.rect.top < 0:
            a2.rect.top = 1
            a2._damage += 5
            a2._veloc_y = random.uniform(0, 1)
        # Marks the lander as crashed if it hits the bottom of the screen
        elif a2.rect.bottom > HEIGHT:
            a2._crashed = True

        # Wraps the lander around left and right edges
        if a2.rect.left < 0:
            a2.rect.right = WIDTH
        elif a2.rect.right > WIDTH:
            a2.rect.left = 0

        # Marks the lander as uncontrollable if damage is at least 100
        if a2._damage >= 100:
            a2._controllable = False

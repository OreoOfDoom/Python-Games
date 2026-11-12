"""Display a spritesheet expanded to a larger size.

"""

import pygame
from pathlib import Path
from .spritesheet import SpriteSheet


class SpriteShow:
    """Class to display an expanded spritesheet.

    Attributes:
        spritesheet (SpriteSheet): The spritesheet object.
        screen_width (int): The width of the display screen.
        screen_height (int): The height of the display screen.
    """

    def __init__(a2, screen,  filename, cellsize, offset=(0, 0)):
        a2.ss = SpriteSheet(filename, cellsize, offset)
        a2.screen = screen
        a2.screen_width, a2.screen_height = screen.get_size()

    def sprite_pos(a2, index):
        """Returns the screen position of a sprite index, where we will draw the sprite."""
        cell_x = a2.ss.cellsize[0] * 2 + 20
        cell_y = a2.ss.cellsize[1] * 2 + 20
        cols = a2.screen_width // cell_x
        row, col = divmod(index, cols)
        x = col * cell_x + 20
        y = row * cell_y + 20
        return x, y

    def draw_sprite(a2, sprite, index):
        x, y = a2.sprite_pos(index)
        a2.screen.blit(sprite, (x, y))

    def text_pos(a2, index):
        x, y = a2.sprite_pos(index)
        return x, y + a2.ss.cellsize[1] * 2 + 3

    def draw_text(a2, text, index):
        x, y = a2.text_pos(index)
        font = pygame.font.Font(None, 20)
        text = font.render(text, True, (255, 255, 255))
        a2.screen.blit(text, (x, y))

    def show(a2):
        a2.screen.fill((0, 0, 0))
        for i in range(a2.ss.num_sprites):
            sprite = a2.ss.image_at(i, colorkey=-1)
            sprite = pygame.transform.scale(sprite, (a2.ss.cellsize[0] * 2, a2.ss.cellsize[1] * 2))
            a2.draw_sprite(sprite, i)
            a2.draw_text(str(i), i)

        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


    
    

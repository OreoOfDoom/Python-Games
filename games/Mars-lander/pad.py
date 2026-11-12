import pygame


class Pad(pygame.sprite.Sprite):
    def __init__(a2, x, y, tall=False):
        pygame.sprite.Sprite.__init__(a2)
        a2.image = pygame.image.load('resources/landing_pads/pad' + ('_tall' if tall else '') + '.png')
        a2.rect = a2.image.get_rect()
        a2.rect.center = (x, y)

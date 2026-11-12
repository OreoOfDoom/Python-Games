import pygame, random, time
from pygame.locals import *
from pathlib import Path

#VARIABLES
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

dd = Path(__file__).parent


wing = dd/'assets/audio/wing.wav'
hit = dd/'assets/audio/hit.wav'

pygame.mixer.init()


class Bird(pygame.sprite.Sprite):

    def __init__(a2):
        pygame.sprite.Sprite.__init__(a2)

        a2.images =  [pygame.image.load(dd/'assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load(dd/'assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load(dd/'assets/sprites/bluebird-downflap.png').convert_alpha()]

        a2.speed = SPEED

        a2.current_image = 0
        a2.image = pygame.image.load(dd/'assets/sprites/bluebird-upflap.png').convert_alpha()
        a2.mask = pygame.mask.from_surface(a2.image)

        a2.rect = a2.image.get_rect()
        a2.rect[0] = SCREEN_WIDHT / 6 # .rect[0] is the x position
        a2.rect[1] = SCREEN_HEIGHT / 2 # .rect[1] is the y position

    def update(a2):
        a2.current_image = (a2.current_image + 1) % 3
        a2.image = a2.images[a2.current_image]
        a2.speed += GRAVITY

        #UPDATE HEIGHT
        a2.rect[1] += a2.speed

    def bump(a2):
        a2.speed = -SPEED

    def begin(a2):
        a2.current_image = (a2.current_image + 1) % 3
        a2.image = a2.images[a2.current_image]




class Pipe(pygame.sprite.Sprite):

    def __init__(a2, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(a2)

        a2. image = pygame.image.load(dd/'assets/sprites/pipe-green.png').convert_alpha()
        a2.image = pygame.transform.scale(a2.image, (PIPE_WIDHT, PIPE_HEIGHT))


        a2.rect = a2.image.get_rect()
        a2.rect[0] = xpos

        if inverted:
            a2.image = pygame.transform.flip(a2.image, False, True)
            a2.rect[1] = - (a2.rect[3] - ysize)
        else:
            a2.rect[1] = SCREEN_HEIGHT - ysize


        a2.mask = pygame.mask.from_surface(a2.image)


    def update(a2):
        a2.rect[0] -= GAME_SPEED # Move the pipe to the left

        

class Ground(pygame.sprite.Sprite):
    
    def __init__(a2, xpos):
        pygame.sprite.Sprite.__init__(a2)
        a2.image = pygame.image.load(dd/'assets/sprites/base.png').convert_alpha()
        a2.image = pygame.transform.scale(a2.image, (GROUND_WIDHT, GROUND_HEIGHT))

        a2.mask = pygame.mask.from_surface(a2.image)

        a2.rect = a2.image.get_rect()
        a2.rect[0] = xpos
        a2.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(a2):
        a2.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

pygame.init()
    
    
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')


BACKGROUND = pygame.image.load(dd / 'assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load(dd/ 'assets/sprites/message.png').convert_alpha()


    
def main():
    
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()

    for i in range (2):
        ground = Ground(GROUND_WIDHT * i)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
    for i in range (2):
        pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])


    clock = pygame.time.Clock()

    begin = True

    while begin:

        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
                    begin = False

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (120, 150))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)

        bird.begin()
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()


    while True:

        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(SCREEN_WIDHT * 2)

            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            pygame.mixer.music.load(hit)
            pygame.mixer.music.play()
            time.sleep(1)
            break

while True:
    main()
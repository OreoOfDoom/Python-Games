#!/usr/bin/env python
""" pygame.examples.chimp

This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


# Import Modules
import os
import pygame as pg

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


# functions to create our resources
def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(a2):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound


# classes for our game objects
class Fist(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    def __init__(a2):
        pg.sprite.Sprite.__init__(a2)  # call Sprite initializer
        a2.image, a2.rect = load_image("fist.png", -1, .5)
        a2.fist_offset = (-235, -80)
        a2.punching = False

    def update(a2):
        """move the fist based on the mouse position"""
        pos = pg.mouse.get_pos()
        a2.rect.topleft = pos
        a2.rect.move_ip(a2.fist_offset)
        if a2.punching:
            a2.rect.move_ip(15, 25)

    def punch(a2, target):
        """returns true if the fist collides with the target"""
        if not a2.punching:
            a2.punching = True
            hitbox = a2.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(a2):
        """called to pull the fist back"""
        a2.punching = False


class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
    monkey when it is punched."""

    def __init__(a2):
        pg.sprite.Sprite.__init__(a2)  # call Sprite initializer
        a2.image, a2.rect = load_image("chimp.png", -1, 2)
        screen = pg.display.get_surface()
        a2.area = screen.get_rect()
        a2.rect.topleft = 10, 90
        a2.move = 18
        a2.dizzy = False

    def update(a2):
        """walk or spin, depending on the monkeys state"""
        if a2.dizzy:
            a2._spin()
        else:
            a2._walk()

    def _walk(a2):
        """move the monkey across the screen, and turn at the ends"""
        newpos = a2.rect.move((a2.move, 0))
        if not a2.area.contains(newpos):
            if a2.rect.left < a2.area.left or a2.rect.right > a2.area.right:
                a2.move = -a2.move
                newpos = a2.rect.move((a2.move, 0))
                a2.image = pg.transform.flip(a2.image, True, False)
        a2.rect = newpos

    def _spin(a2):
        """spin the monkey image"""
        center = a2.rect.center
        a2.dizzy = a2.dizzy + 12
        if a2.dizzy >= 360:
            a2.dizzy = False
            a2.image = a2.original
        else:
            rotate = pg.transform.rotate
            a2.image = rotate(a2.original, a2.dizzy)
        a2.rect = a2.image.get_rect(center=center)

    def punched(a2):
        """this will cause the monkey to start spinning"""
        if not a2.dizzy:
            a2.dizzy = True
            a2.original = a2.image


def main():
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((500, 500), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    pg.mouse.set_visible(False)

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    # Put Text On The Background, Centered
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Pummel The Chimp", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    chimp = Chimp()
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((chimp, fist))
    clock = pg.time.Clock()

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == pg.MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

"""
Main module for the Space Invaders game using Pygame.
"""

import sys

from pygame import sprite, transform, mixer, time, Surface, font, K_RIGHT, K_LEFT, display, image, \
    event, KEYUP, KEYDOWN, K_ESCAPE, K_SPACE, QUIT, init, key

from os.path import abspath, dirname
from random import choice
import asyncio

BASE_PATH = abspath(dirname(__file__))
FONT_PATH = BASE_PATH + "/fonts/"
IMAGE_PATH = BASE_PATH + "/images/"
SOUND_PATH = BASE_PATH + "/sounds/"
SOUND_FORMAT = "ogg"


# Colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)
ORANGE = (255, 149, 14)

SCREEN = display.set_mode((800, 600))
FONT = FONT_PATH + "space_invaders.ttf"
IMG_NAMES = [
    "ship",
    "mystery",
    "enemy1_1",
    "enemy1_2",
    "enemy2_1",
    "enemy2_2",
    "enemy3_1",
    "enemy3_2",
    "explosionblue",
    "explosiongreen",
    "explosionpurple",
    "laser",
    "enemylaser",
]
IMAGES = {
    name: image.load(IMAGE_PATH + "{}.png".format(name)).convert_alpha()
    for name in IMG_NAMES
}

BLOCKERS_POSITION = 450
ENEMY_DEFAULT_POSITION = 65  # Initial value for a new game
ENEMY_MOVE_DOWN = 35
DIFFICULTY_LEVEL = 5  # a value between 1 to 10 - number of enemy bullets


class Ship(sprite.Sprite):
    def __init__(a2):
        sprite.Sprite.__init__(a2)
        a2.image = IMAGES["ship"]
        a2.rect = a2.image.get_rect(topleft=(375, 540))
        a2.speed = 5

    def update(a2, keys, *args):
        if keys[K_LEFT] and a2.rect.x > 10:
            a2.rect.x -= a2.speed
        if keys[K_RIGHT] and a2.rect.x < 740:
            a2.rect.x += a2.speed
        game.screen.blit(a2.image, a2.rect)


class Bullet(sprite.Sprite):
    def __init__(a2, xpos, ypos, direction, speed, filename, side):
        sprite.Sprite.__init__(a2)
        a2.image = IMAGES[filename]
        a2.rect = a2.image.get_rect(topleft=(xpos, ypos))
        a2.speed = speed
        a2.direction = direction
        a2.side = side
        a2.filename = filename

    def update(a2, keys, *args):
        game.screen.blit(a2.image, a2.rect)
        a2.rect.y += a2.speed * a2.direction
        if a2.rect.y < 15 or a2.rect.y > 600:
            a2.kill()


class Enemy(sprite.Sprite):
    def __init__(a2, row, column):
        sprite.Sprite.__init__(a2)
        a2.row = row
        a2.column = column
        a2.images = []
        a2.load_images()
        a2.index = 0
        a2.image = a2.images[a2.index]
        a2.rect = a2.image.get_rect()

    def toggle_image(a2):
        a2.index += 1
        if a2.index >= len(a2.images):
            a2.index = 0
        a2.image = a2.images[a2.index]

    def update(a2, *args):
        game.screen.blit(a2.image, a2.rect)

    def load_images(a2):
        images = {
            0: ["1_2", "1_1"],
            1: ["2_2", "2_1"],
            2: ["2_2", "2_1"],
            3: ["3_1", "3_2"],
            4: ["3_1", "3_2"],
        }
        img1, img2 = (IMAGES["enemy{}".format(img_num)] for img_num in images[a2.row])
        a2.images.append(transform.scale(img1, (40, 35)))
        a2.images.append(transform.scale(img2, (40, 35)))


class EnemiesGroup(sprite.Group):
    def __init__(a2, columns, rows):
        sprite.Group.__init__(a2)
        a2.enemies = [[None] * columns for _ in range(rows)]
        a2.columns = columns
        a2.rows = rows
        a2.leftAddMove = 0
        a2.rightAddMove = 0
        a2.moveTime = 600
        a2.direction = 1
        a2.rightMoves = 30
        a2.leftMoves = 30
        a2.moveNumber = 15
        a2.timer = time.get_ticks()
        a2.bottom = game.enemyPosition + ((rows - 1) * 45) + 35
        a2._aliveColumns = list(range(columns))
        a2._leftAliveColumn = 0
        a2._rightAliveColumn = columns - 1

    def update(a2, current_time):
        if current_time - a2.timer > a2.moveTime:
            if a2.direction == 1:
                max_move = a2.rightMoves + a2.rightAddMove
            else:
                max_move = a2.leftMoves + a2.leftAddMove

            if a2.moveNumber >= max_move:
                a2.leftMoves = 30 + a2.rightAddMove
                a2.rightMoves = 30 + a2.leftAddMove
                a2.direction *= -1
                a2.moveNumber = 0
                a2.bottom = 0
                for enemy in a2:
                    enemy.rect.y += ENEMY_MOVE_DOWN
                    enemy.toggle_image()
                    if a2.bottom < enemy.rect.y + 35:
                        a2.bottom = enemy.rect.y + 35
            else:
                velocity = 10 if a2.direction == 1 else -10
                for enemy in a2:
                    enemy.rect.x += velocity
                    enemy.toggle_image()
                a2.moveNumber += 1

            a2.timer += a2.moveTime

    def add_internal(a2, *sprites):
        super(EnemiesGroup, a2).add_internal(*sprites)
        for s in sprites:
            a2.enemies[s.row][s.column] = s

    def remove_internal(a2, *sprites):
        super(EnemiesGroup, a2).remove_internal(*sprites)
        for s in sprites:
            a2.kill(s)
        a2.update_speed()

    def is_column_dead(a2, column):
        return not any(a2.enemies[row][column] for row in range(a2.rows))

    def random_bottom(a2):
        col = choice(a2._aliveColumns)
        col_enemies = (a2.enemies[row - 1][col] for row in range(a2.rows, 0, -1))
        return next((en for en in col_enemies if en is not None), None)

    def update_speed(a2):
        if len(a2) == 1:
            a2.moveTime = 200
        elif len(a2) <= 10:
            a2.moveTime = 400

    def kill(a2, enemy):
        a2.enemies[enemy.row][enemy.column] = None
        is_column_dead = a2.is_column_dead(enemy.column)
        if is_column_dead:
            a2._aliveColumns.remove(enemy.column)

        if enemy.column == a2._rightAliveColumn:
            while a2._rightAliveColumn > 0 and is_column_dead:
                a2._rightAliveColumn -= 1
                a2.rightAddMove += 5
                is_column_dead = a2.is_column_dead(a2._rightAliveColumn)

        elif enemy.column == a2._leftAliveColumn:
            while a2._leftAliveColumn < a2.columns and is_column_dead:
                a2._leftAliveColumn += 1
                a2.leftAddMove += 5
                is_column_dead = a2.is_column_dead(a2._leftAliveColumn)


class Blocker(sprite.Sprite):
    def __init__(a2, size, color, row, column):
        sprite.Sprite.__init__(a2)
        a2.height = size
        a2.width = size
        a2.color = color
        a2.image = Surface((a2.width, a2.height))
        a2.image.fill(a2.color)
        a2.rect = a2.image.get_rect()
        a2.row = row
        a2.column = column

    def update(a2, keys, *args):
        game.screen.blit(a2.image, a2.rect)


class Mystery(sprite.Sprite):
    def __init__(a2):
        sprite.Sprite.__init__(a2)
        a2.image = IMAGES["mystery"]
        a2.image = transform.scale(a2.image, (75, 35))
        a2.rect = a2.image.get_rect(topleft=(-80, 45))
        a2.row = 5
        a2.moveTime = 25000
        a2.direction = 1
        a2.timer = time.get_ticks()
        a2.mysteryEntered = mixer.Sound(SOUND_PATH + f"mysteryentered.{SOUND_FORMAT}")
        a2.mysteryEntered.set_volume(0.3)
        a2.playSound = True

    def update(a2, keys, currentTime, *args):
        resetTimer = False
        passed = currentTime - a2.timer
        if passed > a2.moveTime:
            if (a2.rect.x < 0 or a2.rect.x > 800) and a2.playSound:
                a2.mysteryEntered.play()
                a2.playSound = False
            if a2.rect.x < 840 and a2.direction == 1:
                a2.mysteryEntered.fadeout(4000)
                a2.rect.x += 2
                game.screen.blit(a2.image, a2.rect)
            if a2.rect.x > -100 and a2.direction == -1:
                a2.mysteryEntered.fadeout(4000)
                a2.rect.x -= 2
                game.screen.blit(a2.image, a2.rect)

        if a2.rect.x > 830:
            a2.playSound = True
            a2.direction = -1
            resetTimer = True
        if a2.rect.x < -90:
            a2.playSound = True
            a2.direction = 1
            resetTimer = True
        if passed > a2.moveTime and resetTimer:
            a2.timer = currentTime


class EnemyExplosion(sprite.Sprite):
    def __init__(a2, enemy, *groups):
        super(EnemyExplosion, a2).__init__(*groups)
        a2.image = transform.scale(a2.get_image(enemy.row), (40, 35))
        a2.image2 = transform.scale(a2.get_image(enemy.row), (50, 45))
        a2.rect = a2.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        a2.timer = time.get_ticks()

    @staticmethod
    def get_image(row):
        img_colors = ["purple", "blue", "blue", "green", "green"]
        return IMAGES["explosion{}".format(img_colors[row])]

    def update(a2, current_time, *args):
        passed = current_time - a2.timer
        if passed <= 100:
            game.screen.blit(a2.image, a2.rect)
        elif passed <= 200:
            game.screen.blit(a2.image2, (a2.rect.x - 6, a2.rect.y - 6))
        elif 400 < passed:
            a2.kill()


class MysteryExplosion(sprite.Sprite):
    def __init__(a2, mystery, score, *groups):
        super(MysteryExplosion, a2).__init__(*groups)
        a2.text = Text(
            FONT, 20, str(score), WHITE, mystery.rect.x + 20, mystery.rect.y + 6
        )
        a2.timer = time.get_ticks()

    def update(a2, current_time, *args):
        passed = current_time - a2.timer
        if passed <= 200 or 400 < passed <= 600:
            a2.text.draw(game.screen)
        elif 600 < passed:
            a2.kill()


class ShipExplosion(sprite.Sprite):
    def __init__(a2, ship, *groups):
        super(ShipExplosion, a2).__init__(*groups)
        a2.image = IMAGES["ship"]
        a2.rect = a2.image.get_rect(topleft=(ship.rect.x, ship.rect.y))
        a2.timer = time.get_ticks()

    def update(a2, current_time, *args):
        passed = current_time - a2.timer
        if 300 < passed <= 600:
            game.screen.blit(a2.image, a2.rect)
        elif 900 < passed:
            a2.kill()


class Life(sprite.Sprite):
    def __init__(a2, xpos, ypos):
        sprite.Sprite.__init__(a2)
        a2.image = IMAGES["ship"]
        a2.image = transform.scale(a2.image, (23, 23))
        a2.rect = a2.image.get_rect(topleft=(xpos, ypos))

    def update(a2, *args):
        game.screen.blit(a2.image, a2.rect)


class Text(object):
    def __init__(a2, textFont, size, message, color, xpos, ypos):
        a2.font = font.Font(textFont, size)
        a2.surface = a2.font.render(message, True, color)
        a2.rect = a2.surface.get_rect(topleft=(xpos, ypos))

    def draw(a2, surface):
        surface.blit(a2.surface, a2.rect)


class SpaceInvaders(object):
    def __init__(a2):
        # It seems, in Linux buffersize=512 is not enough, use 4096 to prevent:
        #   ALSA lib pcm.c:7963:(snd_pcm_recover) underrun occurred
        mixer.pre_init(44100, -16, 1, 4096)
        init()
        a2.clock = time.Clock()
        a2.caption = display.set_caption("Space Invaders")
        a2.screen = SCREEN
        a2.background = image.load(IMAGE_PATH + "background.jpg").convert()
        a2.startGame = False
        a2.mainScreen = True
        a2.gameOver = False
        # Counter for enemy starting position (increased each new round)
        a2.enemyPosition = ENEMY_DEFAULT_POSITION
        a2.titleText = Text(FONT, 50, "Space Invaders", WHITE, 164, 120)
        a2.titleText2 = Text(FONT, 25, "Press any key to continue", WHITE, 201, 205)
        a2.gameOverText = Text(FONT, 50, "Game Over", WHITE, 250, 270)
        a2.nextRoundText = Text(FONT, 50, "Next Round", WHITE, 240, 270)
        a2.enemy1Text = Text(FONT, 25, "   =   10 pts", GREEN, 368, 270)
        a2.enemy2Text = Text(FONT, 25, "   =  20 pts", BLUE, 368, 320)
        a2.enemy3Text = Text(FONT, 25, "   =  30 pts", PURPLE, 368, 370)
        a2.enemy4Text = Text(FONT, 25, "   =  ?????", RED, 368, 420)
        a2.scoreText = Text(FONT, 20, "Score", WHITE, 5, 5)
        a2.livesText = Text(FONT, 20, "Lives ", WHITE, 640, 5)
        
        a2.creator_name = Text(FONT, 20, "Sandy Inspires", GREEN, 600, 570)
        a2.jtl = Text(FONT, 20, "THE LEAGUE", ORANGE, 10, 570)

        a2.life1 = Life(715, 3)
        a2.life2 = Life(742, 3)
        a2.life3 = Life(769, 3)
        a2.livesGroup = sprite.Group(a2.life1, a2.life2, a2.life3)

    def reset(a2, score):
        a2.player = Ship()
        a2.playerGroup = sprite.Group(a2.player)
        a2.explosionsGroup = sprite.Group()
        a2.bullets = sprite.Group()
        a2.mysteryShip = Mystery()
        a2.mysteryGroup = sprite.Group(a2.mysteryShip)
        a2.enemyBullets = sprite.Group()
        a2.make_enemies()
        a2.allSprites = sprite.Group(
            a2.player, a2.enemies, a2.livesGroup, a2.mysteryShip
        )
        a2.keys = key.get_pressed()

        a2.timer = time.get_ticks()
        a2.noteTimer = time.get_ticks()
        a2.shipTimer = time.get_ticks()
        a2.score = score
        a2.create_audio()
        a2.makeNewShip = False
        a2.shipAlive = True

    def make_blockers(a2, number):
        blockerGroup = sprite.Group()
        for row in range(4):
            for column in range(9):
                blocker = Blocker(10, GREEN, row, column)
                blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
                blocker.rect.y = BLOCKERS_POSITION + (row * blocker.height)
                blockerGroup.add(blocker)
        return blockerGroup

    def create_audio(a2):
        a2.sounds = {}
        for sound_name in [
            "shoot",
            "shoot2",
            "invaderkilled",
            "mysterykilled",
            "shipexplosion",
        ]:
            a2.sounds[sound_name] = mixer.Sound(
                SOUND_PATH + "{}.{}".format(sound_name, SOUND_FORMAT)
            )
            a2.sounds[sound_name].set_volume(0.2)

        a2.musicNotes = [
            mixer.Sound(SOUND_PATH + "{}.{}".format(i, SOUND_FORMAT)) for i in range(4)
        ]
        for sound in a2.musicNotes:
            sound.set_volume(0.5)

        a2.noteIndex = 0

    def play_main_music(a2, currentTime):
        if currentTime - a2.noteTimer > a2.enemies.moveTime:
            a2.note = a2.musicNotes[a2.noteIndex]
            if a2.noteIndex < 3:
                a2.noteIndex += 1
            else:
                a2.noteIndex = 0

            a2.note.play()
            a2.noteTimer += a2.enemies.moveTime

    @staticmethod
    def should_exit(evt):
        # type: (pygame.event.EventType) -> bool
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

    def check_input(a2):
        a2.keys = key.get_pressed()
        for e in event.get():
            if a2.should_exit(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(a2.bullets) == 0 and a2.shipAlive:
                        if a2.score <= 100:
                            bullet = Bullet(
                                a2.player.rect.x + 23,
                                a2.player.rect.y + 5,
                                -1,
                                15,
                                "laser",
                                "center",
                            )
                            a2.bullets.add(bullet)
                            a2.allSprites.add(a2.bullets)
                            a2.sounds["shoot"].play()
                        elif a2.score > 100 and a2.score <= 200:
                            leftbullet = Bullet(
                                a2.player.rect.x + 8,
                                a2.player.rect.y + 5,
                                -1,
                                15,
                                "laser",
                                "left",
                            )
                            right_bullet = Bullet(
                                a2.player.rect.x + 38,
                                a2.player.rect.y + 5,
                                -1,
                                15,
                                "laser",
                                "right",
                            )
                            a2.bullets.add(leftbullet)
                            a2.bullets.add(right_bullet)
                            a2.allSprites.add(a2.bullets)
                            a2.sounds["shoot2"].play()

                        else:
                            left_bullet = Bullet(
                                a2.player.rect.x + 8,
                                a2.player.rect.y + 5,
                                -1,
                                15,
                                "laser",
                                "left",
                            )
                            right_bullet = Bullet(
                                a2.player.rect.x + 38,
                                a2.player.rect.y + 5,
                                -1,
                                15,
                                "laser",
                                "right",
                            )
                            center_bullet = Bullet(
                                a2.player.rect.x + 23,
                                a2.player.rect.y + 5,
                                -1,
                                15,
                                "laser",
                                "center",
                            )
                            a2.bullets.add(left_bullet)
                            a2.bullets.add(center_bullet)
                            a2.bullets.add(right_bullet)
                            a2.allSprites.add(a2.bullets)
                            a2.sounds["shoot2"].play()

    def make_enemies(a2):
        enemies = EnemiesGroup(10, 5)
        for row in range(5):
            for column in range(10):
                enemy = Enemy(row, column)
                enemy.rect.x = 157 + (column * 50)
                enemy.rect.y = a2.enemyPosition + (row * 45)
                enemies.add(enemy)

        a2.enemies = enemies

    def make_enemies_shoot(a2):
        if (time.get_ticks() - a2.timer) > 700 and a2.enemies:
            enemy = a2.enemies.random_bottom()
            a2.enemyBullets.add(
                Bullet(
                    enemy.rect.x + 14, enemy.rect.y + 20, 1, 5, "enemylaser", "center"
                )
            )
            a2.allSprites.add(a2.enemyBullets)
            a2.timer = time.get_ticks()

    def calculate_score(a2, row):
        scores = {0: 30, 1: 20, 2: 20, 3: 10, 4: 10, 5: choice([50, 100, 150, 300])}

        score = scores[row]
        a2.score += score
        return score

    def create_main_menu(a2):
        a2.enemy1 = IMAGES["enemy3_1"]
        a2.enemy1 = transform.scale(a2.enemy1, (40, 40))
        a2.enemy2 = IMAGES["enemy2_2"]
        a2.enemy2 = transform.scale(a2.enemy2, (40, 40))
        a2.enemy3 = IMAGES["enemy1_2"]
        a2.enemy3 = transform.scale(a2.enemy3, (40, 40))
        a2.enemy4 = IMAGES["mystery"]
        a2.enemy4 = transform.scale(a2.enemy4, (80, 40))
        a2.screen.blit(a2.enemy1, (318, 270))
        a2.screen.blit(a2.enemy2, (318, 320))
        a2.screen.blit(a2.enemy3, (318, 370))
        a2.screen.blit(a2.enemy4, (299, 420))

    def check_collisions(a2):
        sprite.groupcollide(a2.bullets, a2.enemyBullets, True, True)

        for enemy in sprite.groupcollide(a2.enemies, a2.bullets, True, True).keys():
            a2.sounds["invaderkilled"].play()
            a2.calculate_score(enemy.row)
            EnemyExplosion(enemy, a2.explosionsGroup)
            a2.gameTimer = time.get_ticks()

        for mystery in sprite.groupcollide(
            a2.mysteryGroup, a2.bullets, True, True
        ).keys():
            mystery.mysteryEntered.stop()
            a2.sounds["mysterykilled"].play()
            score = a2.calculate_score(mystery.row)
            MysteryExplosion(mystery, score, a2.explosionsGroup)
            newShip = Mystery()
            a2.allSprites.add(newShip)
            a2.mysteryGroup.add(newShip)

        for player in sprite.groupcollide(
            a2.playerGroup, a2.enemyBullets, True, True
        ).keys():
            if a2.life3.alive():
                a2.life3.kill()
            elif a2.life2.alive():
                a2.life2.kill()
            elif a2.life1.alive():
                a2.life1.kill()
            else:
                a2.gameOver = True
                a2.startGame = False
            a2.sounds["shipexplosion"].play()
            ShipExplosion(player, a2.explosionsGroup)
            a2.makeNewShip = True
            a2.shipTimer = time.get_ticks()
            a2.shipAlive = False

        if a2.enemies.bottom >= 540:
            sprite.groupcollide(a2.enemies, a2.playerGroup, True, True)
            if not a2.player.alive() or a2.enemies.bottom >= 600:
                a2.gameOver = True
                a2.startGame = False

        sprite.groupcollide(a2.bullets, a2.allBlockers, True, True)
        sprite.groupcollide(a2.enemyBullets, a2.allBlockers, True, True)
        if a2.enemies.bottom >= BLOCKERS_POSITION:
            sprite.groupcollide(a2.enemies, a2.allBlockers, False, True)

    def create_new_ship(a2, createShip, currentTime):
        if createShip and (currentTime - a2.shipTimer > 900):
            a2.player = Ship()
            a2.allSprites.add(a2.player)
            a2.playerGroup.add(a2.player)
            a2.makeNewShip = False
            a2.shipAlive = True

    def create_game_over(a2, currentTime):
        a2.screen.blit(a2.background, (0, 0))
        passed = currentTime - a2.timer
        if passed < 750:
            a2.gameOverText.draw(a2.screen)
        elif 750 < passed < 1500:
            a2.screen.blit(a2.background, (0, 0))
        elif 1500 < passed < 2250:
            a2.gameOverText.draw(a2.screen)
        elif 2250 < passed < 2750:
            a2.screen.blit(a2.background, (0, 0))
        elif passed > 3000:
            a2.mainScreen = True

        for e in event.get():
            if a2.should_exit(e):
                sys.exit()

    async def main(a2):
        while True:
            if a2.mainScreen:
                a2.screen.blit(a2.background, (0, 0))
                a2.titleText.draw(a2.screen)
                a2.titleText2.draw(a2.screen)
                a2.enemy1Text.draw(a2.screen)
                a2.enemy2Text.draw(a2.screen)
                a2.enemy3Text.draw(a2.screen)
                a2.enemy4Text.draw(a2.screen)
                a2.creator_name.draw(a2.screen)
                a2.jtl.draw(a2.screen)
                a2.create_main_menu()
                for e in event.get():
                    if a2.should_exit(e):
                        sys.exit()
                    if e.type == KEYUP:
                        # Only create blockers on a new game, not a new round
                        a2.allBlockers = sprite.Group(
                            a2.make_blockers(0),
                            a2.make_blockers(1),
                            a2.make_blockers(2),
                            a2.make_blockers(3),
                        )
                        a2.livesGroup.add(a2.life1, a2.life2, a2.life3)
                        a2.reset(0)
                        a2.startGame = True
                        a2.mainScreen = False

            elif a2.startGame:
                if not a2.enemies and not a2.explosionsGroup:
                    currentTime = time.get_ticks()
                    if currentTime - a2.gameTimer < 3000:
                        a2.screen.blit(a2.background, (0, 0))
                        a2.scoreText2 = Text(FONT, 20, str(a2.score), GREEN, 85, 5)
                        a2.scoreText.draw(a2.screen)
                        a2.scoreText2.draw(a2.screen)
                        a2.nextRoundText.draw(a2.screen)
                        a2.livesText.draw(a2.screen)
                        a2.livesGroup.update()
                        a2.check_input()
                        a2.creator_name.draw(a2.screen)
                        a2.jtl.draw(a2.screen)
                    if currentTime - a2.gameTimer > 3000:
                        # Move enemies closer to bottom
                        a2.enemyPosition += ENEMY_MOVE_DOWN
                        a2.reset(a2.score)
                        a2.gameTimer += 3000
                else:
                    currentTime = time.get_ticks()
                    a2.play_main_music(currentTime)
                    a2.screen.blit(a2.background, (0, 0))
                    a2.allBlockers.update(a2.screen)
                    a2.scoreText2 = Text(FONT, 20, str(a2.score), GREEN, 85, 5)
                    a2.scoreText.draw(a2.screen)
                    a2.scoreText2.draw(a2.screen)
                    a2.livesText.draw(a2.screen)
                    a2.check_input()
                    a2.enemies.update(currentTime)
                    a2.allSprites.update(a2.keys, currentTime)
                    a2.explosionsGroup.update(currentTime)
                    a2.check_collisions()
                    a2.create_new_ship(a2.makeNewShip, currentTime)
                    a2.make_enemies_shoot()
                    a2.creator_name.draw(a2.screen)
                    a2.jtl.draw(a2.screen)

            elif a2.gameOver:
                currentTime = time.get_ticks()
                # Reset enemy starting position
                a2.enemyPosition = ENEMY_DEFAULT_POSITION
                a2.create_game_over(currentTime)

            display.update()
            a2.clock.tick(60)
            await asyncio.sleep(0)


if __name__ == "__main__":
    game = SpaceInvaders()
    asyncio.run(game.main())

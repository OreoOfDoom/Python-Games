import sys
from lander import *
from pad import *
from obstacle import *
from meteor import *
from config import *


class Game:

    def __init__(a2):
        pygame.init()
        pygame.display.set_caption('Mars Lander')
        a2.ticks, a2.time, a2.score, a2.failure_ticks, a2.non_collision_ticks, a2.failure = 0, 0, 0, 0, 0, 0
        a2.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        a2.background_image = pygame.image.load("resources/mars_background.png")
        a2.instruments = pygame.image.load("resources/instruments.png")
        a2.alert_instruments = pygame.image.load("resources/instruments_alert.png")
        # I made the thrust_image same resolution as lander image. As a result,
        # they rotate around the same axis and the flame is always where it should be.
        a2.thrust_image_original = pygame.image.load('resources/thrust.png')
        a2.pad_sprites = pygame.sprite.Group()
        a2.obstacle_sprites = pygame.sprite.Group()
        a2.meteor_sprites = pygame.sprite.Group()
        a2.player_sprite = pygame.sprite.GroupSingle()
        a2.lander = Lander()
        a2.lander_lives = 0
        a2.player_sprite.add(a2.lander)

    def spawn_pads(a2):
        """NUMBER_OF_PADS times spawns a pad randomly on the screen. The pad may be tall or regular.
           It does not overlap with previously spawned pads."""
        a2.pad_sprites.empty()
        while len(a2.pad_sprites) < NUMBER_OF_PADS:
            tall = random.choice([True, False])
            pad = Pad(random.randrange(79, WIDTH - 79), random.randrange(HEIGHT - 200, HEIGHT), tall=tall)
            pad_collision = pygame.sprite.spritecollide(pad, a2.pad_sprites, False)
            if not pad_collision:
                a2.pad_sprites.add(pad)

    def spawn_obstacles(a2):
        """NUMBER_OF_OBSTACLES times spawns an obstacle randomly on screen.
           It does not overlap with previously spawned obstacles."""
        a2.obstacle_sprites.empty()
        number_of_obstacles = random.randint(MIN_OBSTACLES, MAX_OBSTACLES)
        while len(a2.obstacle_sprites) < number_of_obstacles:
            obstacle = Obstacle(random.randrange(0, WIDTH), random.randrange(HEIGHT - 500, HEIGHT))
            obstacle_collision = pygame.sprite.spritecollide(obstacle, a2.obstacle_sprites, False)
            if not obstacle_collision:
                a2.obstacle_sprites.add(obstacle)

    def spawn_meteors(a2, count=random.randint(MIN_METEORS, MAX_METEORS), random_height=False):
        """Spawns a number of meteors, defaultsto a random number between MIN_METEORS and MAX_METEORS.
           These spawn on top of the screen, unless random_height is True. The only time random_height is true
           in this game is at the beginning of each mission, so the game looks more naturally with the meteors already
           flying on the screen."""
        for _ in range(count):
            new_meteor = Meteor(random.randrange(0, WIDTH), random.randrange(0, HEIGHT - 400) if random_height else 0)
            a2.meteor_sprites.add(new_meteor)

    def replace_off_screen_meteors(a2):
        """Deletes a meteor once it flies off the screen, replaces it with a new one."""
        for meteor in a2.meteor_sprites:
            if meteor.is_off_screen():
                meteor.kill()
                a2.spawn_meteors(1)
                del meteor

    def lander_has_both_legs_on_pad(a2, pad_list):
        """Returns True if the lander has both legs on the pad it has landed on and False otherwise."""
        pad = pad_list[0]
        if pad.rect.left <= a2.lander.rect.left and pad.rect.right >= a2.lander.rect.right:
            return True
        return False

    def successful_landing(a2):
        """If the lander has landed successfully, increases the score, displays a message, and starts a new mission.
           The less damage the lander has, the more score is awarded."""
        a2.score += 150 - a2.lander.current_damage()
        a2.reset_lander("Nice landing!")

    def unsuccessful_landing(a2):
        """If the lander has landed unsuccessfully, decreases lives, displays a message, and starts a new mission."""
        a2.lander_lives -= 1
        a2.reset_lander('Unsuccessful landing!')

    def lander_crashed(a2):
        """If the lander has crashed, decreases lives, displays a message, and starts a new mission."""
        a2.lander_lives -= 1
        a2.reset_lander("Lander crashed!")

    def reset_lander(a2, msg=""):
        """Destroys the current lander object, creates a new instance of lander, pauses the game."""
        a2.player_sprite.remove(a2.lander)
        a2.lander = Lander()
        a2.player_sprite.add(a2.lander)
        a2.pause(msg)

    def lander_failure(a2):
        """Unless the lander has already a failure, there is a FAILURE_CHANCE that the lander will suffer a failure
           of a random component from features_list for FAILURE_DURATION. Otherwise decreases the duration of
           current failure."""
        failures_list = ["Right Rotation",
                         "Left Rotation",
                         "Thrust"
                         ]
        if a2.failure_ticks == 0:
            a2.failure = 0
            if random.uniform(0, 1) < FAILURE_CHANCE:
                a2.failure_ticks += FAILURE_DURATION
                a2.failure = random.choice(failures_list)
            return False
        else:
            a2.failure_ticks -= 1
            return True

    def update_lander_meters(a2):
        """Variables stored in hud_components_locations are reassigned to represent actual values
           and then displayed on the screen at their respective coordinates."""
        hud_components_locations = [
            [int(a2.time), (72, 10)],
            [a2.lander.current_fuel(), (72, 32)],
            [a2.lander.current_damage(), (94, 54)],
            [a2.lander.current_altitude(), (258, 10)],
            [a2.lander.current_veloc_x(), (278, 32)],
            [a2.lander.current_veloc_y(), (278, 54)],
            [a2.score, (75, 82)],
            ["Lives: " + str(a2.lander_lives), (1110, 10)],
            ["Meteors: " + str(len(a2.meteor_sprites)), (1110, 32)]
        ]
        for instrument in hud_components_locations:
            a2.show_on_screen(instrument[0], instrument[1])

    def show_on_screen(a2, string, location, font='Arial', font_size=20, colour=WHITE):
        """Shortcut do display a string on a location, with the possibility
           to modify font-face, font-size, and colour."""
        msg = pygame.font.SysFont(font, font_size).render(str(string), True, colour)
        a2.screen.blit(msg, location)

    def update_all_elements(a2):
        """Renders background image, draws every group of sprites on the screen and calls update method where necessary.
           If the lander is faulty or uncontrollable, an error message is displayed and red instrument panel
           is rendered. If the lander is fully functional, the panel is grey. Finally, all instruments are displayed."""
        a2.screen.blit(a2.background_image, (0, 0))
        a2.pad_sprites.draw(a2.screen)
        a2.obstacle_sprites.draw(a2.screen)
        a2.meteor_sprites.update()
        a2.meteor_sprites.draw(a2.screen)
        a2.player_sprite.update()
        a2.player_sprite.draw(a2.screen)
        if not a2.lander.is_controllable():
            a2.screen.blit(a2.alert_instruments, (0, 0))
            a2.show_on_screen("UNCONTROLLABLE", (120, 82))
        elif a2.lander_failure():
            a2.screen.blit(a2.alert_instruments, (0, 0))
            a2.show_on_screen("Failure of " + str(a2.failure), (120, 82))
        else:
            a2.screen.blit(a2.instruments, (0, 0))
        a2.update_lander_meters()

    def pause(a2, msg=""):
        """Pauses the game. A small 'menu' is displayed on a transparent overlay. The player has two options:
           press Enter to continue the game, or press ESC to end the current session."""
        pygame.event.clear()
        a2.update_all_elements()

        # transparent overlay
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((255, 255, 255, 128))
        a2.screen.blit(s, (0, 0))

        a2.show_on_screen(msg, (400, 360), font_size=60, colour=RED)
        a2.show_on_screen("PAUSED", (500, 600), font_size=50)
        a2.show_on_screen("Press Enter to continue", (500, 650), font_size=30)
        a2.show_on_screen("Press ESC to finish game", (500, 680), font_size=30)

        pygame.display.flip()
        while True:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    break
                elif e.key == pygame.K_ESCAPE:
                    a2.end_game()

    def end_game(a2):
        """A menu with black background displayed when the player ends the game manually from pause menu or loses every
           life. Previous score is displayed along with a menu which allows the player to start a new game or exit
           the game completely."""
        pygame.event.clear()
        a2.screen.fill(BLACK)
        a2.show_on_screen("GAME OVER", (500, 600), font_size=50)
        a2.show_on_screen("Press \"N\" to start a new game", (500, 650), font_size=30)
        a2.show_on_screen("Press \"ESC\" to exit", (500, 710), font_size=30)
        a2.show_on_screen("SCORE: " + str(a2.score), (500, 560), font_size=50)
        pygame.display.flip()

        # clears previously pressed key
        pygame.event.wait()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_n:
                    a2.reset_lander()
                    a2.play()

    def lander_collided(a2, dmg):
        """Deals damage to the lander and makes it immune to environmental collisions for NO_COLLISION_DURATION."""
        a2.lander.deal_damage(dmg)
        a2.lander.set_no_collision_duration(NO_COLLISION_DURATION)

    def play(a2):
        """"Main game loop."""

        # set player lives to LANDER_LIVES_START
        a2.lander_lives = LANDER_LIVES_START
        # game runs while the player has at least on life.
        while a2.lander_lives > 0:
            # Spawn static sprites and a set of meteors. The game is paused, a message is displayed.
            a2.spawn_pads()
            a2.spawn_obstacles()
            a2.meteor_sprites.empty()
            a2.spawn_meteors(random_height=True)
            a2.pause("New game")
            while True:
                # This block denotes one tick of a game.
                a2.update_all_elements()
                a2.replace_off_screen_meteors()

                # when meteor collides with a landing pad, the meteor gets destroyed and replaced.
                a2.spawn_meteors(len(pygame.sprite.groupcollide(a2.pad_sprites, a2.meteor_sprites, False, True)))
                # when meteor collides with an obstacle, the meteor gets destroyed and replaced.
                a2.spawn_meteors(
                    len(pygame.sprite.groupcollide(a2.obstacle_sprites, a2.meteor_sprites, False, True)))

                # checks for pressed keys
                pygame.event.pump()
                key = pygame.key.get_pressed()
                if key[pygame.K_p]:
                    a2.pause()
                # right rotation
                if key[pygame.K_RIGHT] and a2.lander.is_controllable() and a2.failure != "Right Rotation":
                    a2.lander.rotate_right()
                # left rotation
                if key[pygame.K_LEFT] and a2.lander.is_controllable() and a2.failure != "Left Rotation":
                    a2.lander.rotate_left()
                # thrust
                if key[pygame.K_SPACE] and a2.lander.is_controllable() and a2.failure != "Thrust" \
                        and a2.lander.current_fuel() >= THRUST_COST:
                    a2.lander.thrust()
                    # rotates thrust_image so it corresponds to lander sprite, then displays it.
                    thrust_image = pygame.transform.rotozoom(a2.thrust_image_original, a2.lander.get_rotation(), 1)
                    a2.screen.blit(thrust_image, (a2.lander.rect.x, a2.lander.rect.y))
                # checks for exit command
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                # check whether the lander has collided with an obstacle
                if a2.lander.can_collide():
                    # if lander collides with an environmental object: destroys the obstacle/meteor hit,
                    # deals damage, makes lander briefly invincible
                    obstacle_collision = pygame.sprite.spritecollide(a2.lander, a2.obstacle_sprites, True)
                    if obstacle_collision:
                        # 10 damage for obstacle collision
                        a2.lander_collided(10)
                    # If a meteor is hit by the player, it is not replaced.
                    # This is done on purpose as it lowers the game's difficulty
                    # as the lander gets damaged. Otherwise it was too complicated to land safely.
                    meteor_collision = pygame.sprite.spritecollide(a2.lander, a2.meteor_sprites, True)
                    if meteor_collision:
                        # 25 damage for meteor collision
                        a2.lander_collided(25)
                else:
                    # decrease lander's invincibility ticks.
                    a2.lander.decrease_no_collision_duration()

                # Displays 'NOCOL' on the instruments panel if the lander has recently hit an object
                # and is still immune to collisions.
                if not a2.lander.can_collide() and a2.lander.is_controllable():
                    a2.show_on_screen("NOCOL", (290, 10), colour=GREEN)

                # checks whether the lander has landed
                landed = pygame.sprite.spritecollide(a2.lander, a2.pad_sprites, False)
                if landed:
                    if a2.lander.has_safe_landing_speed() and a2.lander.is_horizontal() \
                            and a2.lander_has_both_legs_on_pad(landed):
                        a2.successful_landing()
                    else:
                        a2.unsuccessful_landing()
                    break
                # Check if lander has hit lower bound of the screen.
                elif a2.lander.is_crashed():
                    a2.lander_crashed()
                    break

                # Significantly increases gravity once the lander has reached 100% damage. This is done so the
                # player doesn't have to wait ages for a new mission once their lander has been destroyed.
                if not a2.lander.is_controllable():
                    for _ in range(3):
                        a2.lander.count_for_gravity()

                # Update the displayed image, increase ticks counter and update time counter which is based on it.
                pygame.display.flip()
                a2.ticks += 1
                a2.time = a2.ticks / 30
        # conclude game
        a2.end_game()

"""
Gravity bounce in Object Oriented style

This version of the gravity bounce program uses an object oriented style to
organize the code. The main game loop is in the Game class, and the player is
a separate class. This makes the code easier to read and understand, and
allows for more complex games with multiple objects.

## Assignment 5

1. Open `03_gravity_bounce_obj.py` 
2. Review the program and try to understand how it works.
3. Change the program so that the player's initial velocity and position are set
   in the initializer to the `Player` class. 
4. Add a color for the player, configurable in the initializer.
5. Add a second player to the game. The second player should be a different
   color and have different initial position and velocity.

When you are done, your program should have two player objects ( but only one
Player class!), of different colors, bouncing around in different trajectories. 

"""
import pygame


class Colors:
    """Constants for Colors"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)


class GameSettings:
    """Settings for the game"""
    width: int = 500
    height: int = 500
    player_width: int = 20
    player_height: int = 20

    player_start_x: int = 100
    player_start_y: int = None

    gravity: float = 200
    v_0_y: float = 0  # Initial y velocity
    v_0_x: float = 75 # Initial x velocity

    jump_v_y: float = 400

    FPS = 30
    d_t = 1 / FPS # Time step


class Game:
    """Main object for the top level of the game. Holds the main loop and other
    update, drawing and collision methods that operate on multiple other
    objects, like the player and obstacles."""
    
    def __init__(a2, settings: GameSettings):
        pygame.init()

        a2.settings = settings
        a2.running = True

        a2.screen = pygame.display.set_mode((a2.settings.width, a2.settings.height))
        a2.clock = pygame.time.Clock()

        a2.players = []

    def add_player(a2, player):
        a2.players.append(player)


    def run(a2):
        """Main game loop"""

        while a2.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    a2.running = False

            a2.screen.fill(Colors.WHITE)

            for player in a2.players:
                player.update()
                player.draw(a2.screen)
                
            pygame.display.flip()
            a2.clock.tick(a2.settings.FPS)

        pygame.quit()


class Player:
    """Player class, just a bouncing rectangle"""

    def __init__(a2, game: Game):
        a2.game = game
        settings = game.settings

        a2.width = settings.player_width
        a2.height = settings.player_height
      
        a2.is_jumping = False
        a2.v_jump = settings.jump_v_y

        a2.y = settings.player_start_y if settings.player_start_y is not None else settings.height - a2.height
        a2.x = settings.player_start_x
        
        a2.v_x = settings.v_0_x  # X Velocity
        a2.v_y = settings.v_0_y  # Y Velocity

    def update(a2):
        """Update player position, continuously jumping"""
        a2.update_jump()
        a2.update_y()
        a2.update_x()

    def update_y(a2):
        """Update the player's y position based on gravity and velocity"""
        a2.v_y += a2.game.settings.gravity * a2.game.settings.d_t # Add gravity to the y velocity
        a2.y += a2.v_y * a2.game.settings.d_t # Update the player's y position, based on the current velocity

        if a2.y >= a2.game.settings.height - a2.height:
            a2.y = a2.game.settings.height - a2.height
            a2.v_y = 0
            a2.is_jumping = False

    def update_x(a2):
        """Update the player's x position based on horizontal velocity and bounce on edges"""
        a2.x += a2.v_x * a2.game.settings.d_t  # Update the player's x position based on the current velocity

        if a2.x <= 0:
            a2.x = 0
            a2.v_x = -a2.v_x
        elif a2.x >= a2.game.settings.width - a2.width:
            a2.x = a2.game.settings.width - a2.width
            a2.v_x = -a2.v_x

    def update_jump(a2):
        """Handle the player's jumping logic"""
        
        if not a2.is_jumping:
            a2.v_y = -a2.v_jump
            a2.is_jumping = True

    def draw(a2, screen):
        pygame.draw.rect(screen, Colors.BLACK, (a2.x, a2.y, a2.width, a2.height))


settings = GameSettings()
game = Game(settings)

p1 = Player(game)
game.add_player(p1)


game.run()

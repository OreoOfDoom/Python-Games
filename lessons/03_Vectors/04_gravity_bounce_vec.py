"""
Gravity bounce using Vectors. 

This version of the Gravity Bounce program uses Pygame's Vector2 class to handle
the player's position and velocity. This makes the code more readable and
understandable, and makes it easier to add more complex features to the game.


"""
import pygame
from dataclasses import dataclass


class Colors:
    """Constants for Colors"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (255, 255, 255)


@dataclass
class GameSettings:
    """Settings for the game"""
    width: int = 500
    height: int = 500
    gravity: float = 0.3
    player_start_x: int = 100
    player_start_y: int = None
    player_v_y: float = 0  # Initial y velocity
    player_v_x: float = 4  # Initial x velocity
    player_width: int = 20
    player_height: int = 20
    player_jump_velocity: float = 15
    frame_rate: int = 15


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

        # Turn Gravity into a vector
        a2.gravity = pygame.Vector2(0, a2.settings.gravity)

    def run(a2):
        """Main game loop"""
        player = Player(a2)

        while a2.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    a2.running = False

            player.update()

            a2.screen.fill(Colors.BACKGROUND_COLOR)
            player.draw(a2.screen)
            pygame.display.flip()
            a2.clock.tick(a2.settings.frame_rate)

        pygame.quit()


class Player:
    """Player class, just a bouncing rectangle"""

    def __init__(a2, game: Game):
        a2.game = game
        settings = a2.game.settings

        a2.width = settings.player_width
        a2.height = settings.player_height
    
        # Vector for our jump velocity, which is just up
        a2.v_jump = pygame.Vector2(0, -settings.player_jump_velocity)

        # Player position
        a2.pos = pygame.Vector2(settings.player_start_x, 
                                  settings.player_start_y if settings.player_start_y is not None else settings.height - a2.height)
        
        # Player's velocity
        a2.vel = pygame.Vector2(settings.player_v_x, settings.player_v_y)  # Velocity vector



    # Direction functions. IMPORTANT! Using these functions isn't really
    # necessary, but it makes the code more readable. You could just use
    # a2.vel.x < 0, but writing "a2.going_left()" is a lot easier to read and
    # understand, it makes the code a2-documenting. 

    def going_up(a2):
        """Check if the player is going up"""
        return a2.vel.y < 0
    
    def going_down(a2):
        """Check if the player is going down"""
        return a2.vel.y > 0
    
    def going_left(a2):
        """Check if the player is going left"""
        return a2.vel.x < 0
    
    def going_right(a2):
        """Check if the player is going right"""
        return a2.vel.x > 0
    
    
    # Location Fuctions
    
    def at_top(a2):
        """Check if the player is at the top of the screen"""
        return a2.pos.y <= 0
    
    def at_bottom(a2):
        """Check if the player is at the bottom of the screen"""
        return a2.pos.y >= a2.game.settings.height - a2.height

    def at_left(a2):
        """Check if the player is at the left of the screen"""
        return a2.pos.x <= 0
    
    def at_right(a2):
        """Check if the player is at the right of the screen"""
        return a2.pos.x >= a2.game.settings.width - a2.width
    
    # Updates
    
    def update(a2):
        """Update player position, continuously jumping"""
        a2.update_jump()
        a2.update_v()
        a2.update_pos()
        
    def update_v(a2):
        """Update the player's velocity based on gravity and bounce on edges"""
         
        a2.vel += a2.game.gravity  # Add gravity to the velocity

        if a2.at_bottom() and a2.going_down():
            a2.vel.y = 0

        if a2.at_top() and a2.going_up():
            a2.vel.y = -a2.vel.y # Bounce off the top. 

        # If the player hits one side of the screen or the other, bounce the
        # player. we are also checking if the player has a velocity going farther
        # off the screeen, because we don't want to bounce the player if it's
        # already going away from the edge
        
        if (a2.at_left() and a2.going_left() ) or ( a2.at_right() and a2.going_right()):
            a2.vel.x = -a2.vel.x
            
    def update_pos(a2):
        """Update the player's position based on velocity"""
        a2.pos += a2.vel  # Update the player's position based on the current velocity

        # If the player is at the bottom, stop the player from falling and
        # stop the jump
        
        if a2.at_bottom():
            a2.pos.y = a2.game.settings.height - a2.height

        if a2.at_top():
            a2.pos.y = 0

        # Don't let the player go off the left side of the screen
        if a2.at_left():
            a2.pos.x = 0
  
        # Don't let the player go off the right side of the screen
        elif a2.at_right():
            a2.pos.x = a2.game.settings.width - a2.width

    def update_jump(a2):
        """Handle the player's jumping logic"""
        
        # Notice that we've gotten rid of a2.is_jumping, because we can just
        # check if the player is at the bottom. 
        if a2.at_bottom():
            a2.vel += a2.v_jump
         

    def draw(a2, screen):
        pygame.draw.rect(screen, Colors.PLAYER_COLOR, (a2.pos.x, a2.pos.y, a2.width, a2.height))


settings = GameSettings()
game = Game(settings)
game.run()

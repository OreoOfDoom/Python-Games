import pygame
import random
from pathlib import Path

d = Path(__file__).parent # The directory that holds the script

# Initialize Pygame
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PLAYER_SIZE = 50
    OBSTACLE_WIDTH = 50
    OBSTACLE_HEIGHT = 50
    OBSTACLE_SPEED = 10
    GRAVITY = 1
    JUMP_STRENGTH = 15
    BACKGROUND_SCROLL_SPEED = 2
    FPS = 30

# Initialize screen
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

# Define background class
class Background(pygame.sprite.Sprite):
    """Represents the scrolling background in the game."""
    def __init__(a2):
        super().__init__()
        
        # The Sprite image is 2x as wide as the screen
        a2.image = pygame.Surface((Settings.SCREEN_WIDTH * 2, Settings.SCREEN_HEIGHT))
        
        # Load the background image and scale it to the screen size. Note the convert() call. 
        # This converts the form of the image to be more efficient. 
        orig_image= pygame.image.load(d/'assets/background.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        
        # Then, copy it into the a2.image surface twice
        a2.image.blit(orig_image, (0, 0))
        a2.image.blit(orig_image, (Settings.SCREEN_WIDTH, 0))
        
        a2.rect = a2.image.get_rect()
        a2.rect.x = 0
        a2.rect.y = 0

    def update(a2):
        """Update the position of the background."""
        
        a2.rect.x -= Settings.BACKGROUND_SCROLL_SPEED
        
        if a2.rect.right <= Settings.SCREEN_WIDTH:
            a2.rect.x = 0

# Define player class
class Player(pygame.sprite.Sprite):
    """Represents the player in the game."""
    def __init__(a2):
        super().__init__()
        a2.image = pygame.Surface((Settings.PLAYER_SIZE, Settings.PLAYER_SIZE))
        a2.image.fill(Settings.BLACK)
        a2.rect = a2.image.get_rect()
        a2.rect.x = 100
        a2.rect.y = Settings.SCREEN_HEIGHT - Settings.PLAYER_SIZE
        a2.y_velocity = 0
        a2.is_jumping = False

    def update(a2):
        """Update the player's position."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not a2.is_jumping:
            a2.y_velocity = -Settings.JUMP_STRENGTH
            a2.is_jumping = True

        a2.y_velocity += Settings.GRAVITY
        a2.rect.y += a2.y_velocity

        if a2.rect.bottom >= Settings.SCREEN_HEIGHT:
            a2.rect.bottom = Settings.SCREEN_HEIGHT
            a2.y_velocity = 0
            a2.is_jumping = False


class Obstacle(pygame.sprite.Sprite):
    """Represents an obstacle in the game."""
    def __init__(a2):
        super().__init__()
        a2.image = pygame.Surface((Settings.OBSTACLE_WIDTH, Settings.OBSTACLE_HEIGHT))
        a2.image.fill(Settings.BLACK)
        a2.rect = a2.image.get_rect()
        a2.rect.x = Settings.SCREEN_WIDTH
        a2.rect.y = Settings.SCREEN_HEIGHT - Settings.OBSTACLE_HEIGHT

    def update(a2):
        """Update the position of the obstacle."""
        a2.rect.x -= Settings.OBSTACLE_SPEED
        if a2.rect.x + Settings.OBSTACLE_WIDTH <= 0:
            a2.kill()


class Game:
    """Represents the main game."""
    def __init__(a2):
        """Initialize the game, create game objects, and set up the game environment."""
        # Create sprite groups
        a2.all_sprites = pygame.sprite.Group()
        a2.obstacles = pygame.sprite.Group()

        # Create background instance and add to sprite group
        a2.background = Background()
        a2.all_sprites.add(a2.background)

        # Create player instance and add to sprite group
        a2.player = Player()
        a2.all_sprites.add(a2.player)

        # Score
        a2.score = 0
        a2.font = pygame.font.SysFont(None, 48)

        # Clock
        a2.clock = pygame.time.Clock()

    def run(a2):
        """Run the main game loop."""
        running = True
        obstacle_counter = 0 #Enforce a min number of frames between obstacles. 

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            a2.all_sprites.update()

            # Draw everything
            a2.all_sprites.draw(screen)

            # Spawn obstacles. The `obstacle_counter` is used to enforce a
            # minimum number of frames between obstacles. The  `
            # obstacle_counter % 30 == 0` means that there is an
            # opportunity to spawn an obstacle every 30 frames , but the actual
            # spawn rate is controlled by the random.random() call. So this code
            # has a 40% chance of spawning an obstacle every 30 frames.
            if random.random() <= .4 and obstacle_counter % 30 == 0:
                obstacle = Obstacle()
                a2.obstacles.add(obstacle)
                a2.all_sprites.add(obstacle)
          
            obstacle_counter += 1

            # Check for collisions
            if (collider := pygame.sprite.spritecollideany(a2.player, a2.obstacles)):
                collider.image.fill((255, 0, 0))  # Make sprites red when they collide

            # Draw score
            a2.score += 1
            score_text = a2.font.render(f"Score: {a2.score}", True, Settings.BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            
            a2.clock.tick(Settings.FPS)

        pygame.quit()


def main():
    """Create a game instance and run it."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

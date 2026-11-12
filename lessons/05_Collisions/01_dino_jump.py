"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Jump")

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS
FPS = 60

# Player attributes
PLAYER_SIZE = 25

player_speed = 5

# Obstacle attributes
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 20
obstacle_speed = 5

# Font
font = pygame.font.SysFont(None, 36)


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(a2):
        super().__init__()
        a2.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        a2.image.fill(BLACK)
        a2.rect = a2.image.get_rect()
        a2.rect.x = WIDTH
        a2.rect.y = HEIGHT - OBSTACLE_HEIGHT - 10

        a2.explosion = pygame.image.load(images_dir / "explosion1.gif")

    def update(a2):
        a2.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if a2.rect.right < 0:
            a2.kill()

    def explode(a2):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        a2.image = a2.explosion
        a2.image = pygame.transform.scale(a2.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        a2.rect = a2.image.get_rect(center=a2.rect.center)


# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(a2):
        super().__init__()
        a2.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        a2.image.fill(BLUE)
        a2.rect = a2.image.get_rect()
        a2.rect.x = 50
        a2.rect.y = HEIGHT - PLAYER_SIZE - 10
        a2.speed = player_speed

    def update(a2):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            a2.rect.y -= a2.speed
        if keys[pygame.K_DOWN]:
            a2.rect.y += a2.speed

        # Keep the player on screen
        if a2.rect.top < 0:
            a2.rect.top = 0
        if a2.rect.bottom > HEIGHT:
            a2.rect.bottom = HEIGHT

# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)

# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    if random.random() < 0.4:
        obstacle = Obstacle()
        obstacles.add(obstacle)
        return 1
    return 0


# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()

    player = Player()

    obstacle_count = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update player
        player.update()

        # Add obstacles and update
        if pygame.time.get_ticks() - last_obstacle_time > 500:
            last_obstacle_time = pygame.time.get_ticks()
            obstacle_count += add_obstacle(obstacles)
        
        obstacles.update()

        # Check for collisions
        collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
        if collider:
            collider[0].explode()
       
        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, player)
        obstacles.draw(screen)

        # Display obstacle count
        obstacle_text = font.render(f"Obstacles: {obstacle_count}", True, BLACK)
        screen.blit(obstacle_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    # Game over screen
    screen.fill(WHITE)

if __name__ == "__main__":
    game_loop()

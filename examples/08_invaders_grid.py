"""
Example of how to draw a space invaders enemy grid. 

"""
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders Enemy Grid")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Enemy class definition
class Enemy:
    def __init__(a2, x, y):
        a2.rect = pygame.Rect(x, y, 30, 10)  # Create a 30x10 rectangle at (x, y)

    def draw(a2, surface):
        pygame.draw.rect(surface, red, a2.rect)  # Draw the enemy rectangle in red

# Function to create a 6x4 grid of enemies
def create_enemies():
    enemies = []
    start_x = 50
    start_y = 50
    spacing_x = 40  # Spacing between enemies horizontally
    spacing_y = 30  # Spacing between enemies vertically

    # Create 6 columns and 4 rows of enemies
    for row in range(4):
        for col in range(6):
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            enemy = Enemy(x, y)
            enemies.append(enemy)
    return enemies

# Create enemies
enemies = create_enemies()

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(white)

    # Draw all enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

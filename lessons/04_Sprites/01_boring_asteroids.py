import pygame
import math

# Settings class to store game configuration
class Settings:
    def __init__(a2):
        a2.width = 800
        a2.height = 600
        a2.fps = 60
        a2.triangle_size = 20
        a2.projectile_speed = 5
        a2.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0)
        }

# Spaceship class to handle player movement and drawing
class Spaceship:
    def __init__(a2, settings):
        a2.settings = settings
        a2.position = pygame.Vector2(a2.settings.width // 2, a2.settings.height // 2)
        a2.angle = 0

    def handle_input(a2):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            a2.angle -= 5
        if keys[pygame.K_RIGHT]:
            a2.angle += 5

    def draw(a2, surface):
        points = [
            pygame.Vector2(0, -a2.settings.triangle_size),  # top point
            pygame.Vector2(-a2.settings.triangle_size / 2, a2.settings.triangle_size),  # left side point
            pygame.Vector2(a2.settings.triangle_size / 2, a2.settings.triangle_size)  # right side point
        ]
        rotated_points = [point.rotate(a2.angle) + a2.position for point in points]
        pygame.draw.polygon(surface, a2.settings.colors['white'], rotated_points)

# Projectile class to handle projectile movement and drawing
class Projectile:
    def __init__(a2, position, angle, settings):
        a2.position = position.copy()
        a2.direction = pygame.Vector2(0, -1).rotate(angle)
        a2.settings = settings

    def move(a2):
        a2.position += a2.direction * a2.settings.projectile_speed

    def draw(a2, surface):
        pygame.draw.circle(surface, a2.settings.colors['red'], (int(a2.position.x), int(a2.position.y)), 5)

# Game class to manage the game loop and objects
class Game:
    def __init__(a2):
        pygame.init()
        a2.settings = Settings()
        a2.screen = pygame.display.set_mode((a2.settings.width, a2.settings.height))
        pygame.display.set_caption("Really Boring Asteroids")
        a2.clock = pygame.time.Clock()
        a2.running = True
        a2.spaceship = Spaceship(a2.settings)
        a2.projectiles = []

    def handle_events(a2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a2.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create and fire a projectile
                    new_projectile = Projectile(a2.spaceship.position, a2.spaceship.angle, a2.settings)
                    a2.projectiles.append(new_projectile)

    def update(a2):
        # Update spaceship
        a2.spaceship.handle_input()

        # Update projectiles
        for projectile in a2.projectiles[:]:
            projectile.move()
            if not (0 <= projectile.position.x <= a2.settings.width) or not (0 <= projectile.position.y <= a2.settings.height):
                a2.projectiles.remove(projectile)

    def draw(a2):
        a2.screen.fill(a2.settings.colors['black'])
        a2.spaceship.draw(a2.screen)
        for projectile in a2.projectiles:
            projectile.draw(a2.screen)
        pygame.display.flip()

    def run(a2):
        while a2.running:
            a2.handle_events()
            a2.update()
            a2.draw()
            a2.clock.tick(a2.settings.fps)
        pygame.quit()

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()

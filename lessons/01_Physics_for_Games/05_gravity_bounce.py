"""
Gravity bounce with x motion

If we add X velocity, from side to side, the player will bounce around the
screen. We will need to add a check to see if the player hits the left or right
side of the screen.

"""
import pygame
from dataclasses import dataclass

@dataclass
class GameSettings:
    """Class for keeping track of game settings and constants."""
    screen_width: int = 500
    screen_height: int = 500
    square_size: int = 20
    square_color: tuple = (0, 0, 0)  # Black
    background_color: tuple = (255, 255, 255)  # White
    fps: int = 30
    gravity: float = 60.0  # Acceleration due to gravity
    drag: float = 100.0
    jump_velocity_y: float =  200.0  # Initial jump velocity in y direction
    jump_velocity_x: float =  0  # Initial jump velocity in x direction
    d_t: float = 1.0/30  # Time step for physics calculations
    x_speed = 10
    

# Initialize Pygame
pygame.init()

# Initialize game settings
settings = GameSettings()

# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("It bounces now")

# Square starting position
x_pos = 430
y_pos = settings.screen_height - settings.square_size

# Initial velocities  
velocity_x = 0
velocity_y = 0
x_direction = 1  # Either 1 or -1, to keep track of direction after hitting the ground

is_jumping = False

# Main loop
running = True
clock = pygame.time.Clock()
velocity_y = 0
velocity_x = 0
d_x = 0
jump_velocity_y = 200
yesjump = input("Do you want to auto jump? Yes or no? Please type yes or no.\n By the way, it wont work if you type in an invalid option.")
print("Ok")

while running:
    
    
    jump_velocity_yy = settings.jump_velocity_y * 0.99955
    settings.jump_velocity_y = jump_velocity_yy
    # Handle events, such as quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Continuously jump. If the square is not jumping, make it jump
    if is_jumping is False and yesjump == ("no"):
    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] :
        # Jumping means that the square is going up. The top of the 
        # screen is y=0, and the bottom is y=screen_height. So, to go up,
        # we need to have a negative y velocity

            velocity_y = -settings.jump_velocity_y
            velocity_x = settings.jump_velocity_x * x_direction
            is_jumping = True
    if is_jumping is False and yesjump == ("yes"):
    
        # Jumping means that the square is going up. The top of the 
        # screen is y=0, and the bottom is y=screen_height. So, to go up,
        # we need to have a negative y velocity

            velocity_y = -settings.jump_velocity_y
            velocity_x = settings.jump_velocity_x * x_direction
            is_jumping = True

            
            

  

       
       
    else: # the square is jumping
        # Update square position. Gravity is always pulling the square down,
        # which is the positive y direction, so we add settings.gravity to the y velocity
        # to make the square go up more slowly. Eventually, the square will have
        # a positive y velocity, and gravity will pull the square down.




        velocity_y += settings.gravity * settings.d_t
        #Make a drag function  
        if velocity_x >0:
            velocity_x -= settings.drag * settings.d_t
        if velocity_x <0:
            velocity_x += settings.drag * settings.d_t
        if velocity_x > 0 and velocity_x < 0.1:
            velocity_x =0
        if velocity_x < 0 and velocity_x > 0.1:
            velocity_x = 0
        # if velocity_y >0:
        #     velocity_y -= settings.drag * settings.d_t
        # if velocity_y <0:
        #     velocity_y += settings.drag * settings.d_t
        # if velocity_y <0.1:
        #     velocity_y =0
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            velocity_x -= settings.x_speed
          
            
            
        if keys[pygame.K_RIGHT]:
            velocity_x += settings.x_speed

        # Update the position with the velocity. Like with the velocity, we change
        # the position by adding the velocity, not setting it to the velocity, and
        # we change it a bit each frame.
        y_pos += velocity_y * settings.d_t
        x_pos += velocity_x * settings.d_t
           
                        
            
       
    acceleration = .1
    keys = pygame.key.get_pressed()
    
        
        
        

    # If the square hits one side of the screen or the other, bounce the square
    if x_pos <= 0 or x_pos + settings.square_size >= settings.screen_width:
        velocity_x = -velocity_x
        
        # Update direction tracking
        x_direction = -x_direction 
        # This way is more reliable, since it will always be 1 or -1 and direction is tied to velocity
        if velocity_x != 0:
            x_direction = int(velocity_x / abs(velocity_x))

    # If the square hits the top of the screen, bounce the square
    if y_pos <= 0:
        velocity_y = -velocity_y

    # If the square hits the ground, stop the square from falling.
    if y_pos + settings.square_size > settings.screen_height:
        y_pos = settings.screen_height - settings.square_size
        velocity_y = 0
        velocity_x = 0
        is_jumping = False

    # Fill the screen with background color (clears previous frame)
    screen.fill(settings.background_color)

    # Draw the square
    pygame.draw.rect(screen, settings.square_color, (x_pos, y_pos, settings.square_size, settings.square_size))

    # Update the display
    pygame.display.flip()

    # Frame rate control
    clock.tick(settings.fps)

pygame.quit()

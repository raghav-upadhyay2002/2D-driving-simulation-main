import pygame
import sys
from car_physics import Car  
import os

pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('City Simulation with Traffic Light and Physics-based Car')


PPU = 32 

def city_layout(screen):
    white = (255, 255, 255)
    road_color = (52, 52, 52)
    line_color = (200, 200, 200)
    screen.fill(white)
    
    # Draw main roads
    pygame.draw.rect(screen, road_color, (0, 300, width, 200)) 
    pygame.draw.rect(screen, road_color, (400, 0, 200, height))  
    
    # Draw dashed lane dividers for vertical and horizontal roads
    dash_length = 20
    gap_length = 20

    # Vertical dashed line (centered on the vertical road)
    for y in range(0, height, dash_length + gap_length): 
        pygame.draw.line(screen, line_color, (500, y), (500, y + dash_length), 2)  
    # Horizontal dashed line (centered on the horizontal road)
    for x in range(0, width, dash_length + gap_length):
        pygame.draw.line(screen, line_color, (x, 400), (x + dash_length, 400), 2)  
def draw_car(screen, car, car_image):
    rotated_image = pygame.transform.rotate(car_image, car.angle)
    rect = rotated_image.get_rect(center=(car.position.x * PPU, car.position.y * PPU))
    screen.blit(rotated_image, rect.topleft)

# Load the car image
current_dir = os.path.dirname(os.path.abspath(__file__))
car_image_path = os.path.join(current_dir, "car.png")
car_image = pygame.image.load(car_image_path)

# Initialize the car
car = Car(5, 5)  # Start position at (5,5) in world units

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.get_time() / 1000  # Get delta time in seconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # User input for car control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.acceleration = car.max_acceleration
    elif keys[pygame.K_DOWN]:
        car.acceleration = -car.max_acceleration
    else:
        car.acceleration = 0

    if keys[pygame.K_LEFT]:
        car.steering = car.max_steering
    elif keys[pygame.K_RIGHT]:
        car.steering = -car.max_steering
    else:
        car.steering = 0

    # Update car physics
    car.update(dt)

    # Drawing
    city_layout(screen)
    draw_car(screen, car, car_image)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
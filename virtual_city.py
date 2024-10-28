import pygame
import sys
from car_physics import Car  
import os

pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('City Simulation with Traffic Light and Physics-based Car')

PPU = 32 

# Traffic light configuration
traffic_light_position = (370, 500) 
light_cycle_time = 5000 
traffic_light_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]  
current_light = 0
light_timer = 0

font = pygame.font.Font(None, 36)

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

def draw_traffic_light(screen, position, color):
    pygame.draw.rect(screen, color, (*position, 20, 60))

def render_hud(screen, car):
    speed_text = f"Speed: {car.velocity.length():.2f}"
    position_text = f"Position: ({car.position.x:.1f}, {car.position.y:.1f})"
    text = font.render(f"{speed_text} | {position_text}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def draw_car(screen, car, car_image):
    rotated_image = pygame.transform.rotate(car_image, car.angle)
    rect = rotated_image.get_rect(center=(car.position.x * PPU, car.position.y * PPU))
    screen.blit(rotated_image, rect.topleft)

# Load the car image
current_dir = os.path.dirname(os.path.abspath(__file__))
car_image_path = os.path.join(current_dir, "car.png")
car_image = pygame.image.load(car_image_path)

# Initialize the car
car = Car(2, 14)  


# Main loop
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.get_time() / 1000  

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
        if abs(car.velocity.x) > car.free_deceleration * dt:
            car.acceleration = -car.free_deceleration if car.velocity.x > 0 else car.free_deceleration
        else:
            car.acceleration = 0
            car.velocity.x = 0  # Stop the car if it's moving very slowly

    if keys[pygame.K_LEFT]:
        car.steering = car.max_steering
    elif keys[pygame.K_RIGHT]:
        car.steering = -car.max_steering
    else:
        car.steering = 0    
        

    # Update car physics
    car.update(dt)

    # Update traffic light
    light_timer += dt * 1000  # Convert dt to milliseconds
    if light_timer >= light_cycle_time:
        current_light = (current_light + 1) % len(traffic_light_colors)
        light_timer = 0  # Fixed typo here

    # Drawing
    city_layout(screen)
    draw_traffic_light(screen, traffic_light_position, traffic_light_colors[current_light])
    draw_car(screen, car, car_image)
    render_hud(screen, car)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
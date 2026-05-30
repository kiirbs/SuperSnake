import pygame
import random

import settings
from food import generate_food

# Setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
move_timer = 0
score = 0

width = screen.get_width()
height = screen.get_height()

# Grid
grid_size = settings.DEFAULT_GRID_SIZE
cell_size = min(width, height) // grid_size

# Snake
snake_head = [
    random.randint(2, grid_size - 3), 
    random.randint(2, grid_size - 3)
]
snake = []
snake.append(snake_head)
direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

# Food
food_pos = generate_food(grid_size, snake)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and direction != "DOWN":
                direction = "UP"
            
            elif event.key == pygame.K_s and direction != "UP":
                direction = "DOWN"
                
            elif event.key == pygame.K_q and direction != "RIGHT":
                direction = "LEFT"
                
            elif event.key == pygame.K_d and direction != "LEFT":
                direction = "RIGHT"
            
    screen.fill(settings.BACKGROUND_COLOR)
    
    grid_offset_x = (width - grid_size * cell_size) / 2
    grid_offset_y = (height - grid_size * cell_size) / 2

    for row in range(grid_size):
        for col in range(grid_size):
            
            x = grid_offset_x + col * cell_size
            y = grid_offset_y + row * cell_size
            
            pygame.draw.rect(screen, settings.GRID_COLOR, (x, y, cell_size, cell_size), 1)
            
    snake_row = snake_head[0]
    snake_col = snake_head[1]
    food_row = food_pos[0]
    food_col = food_pos[1]
            
    pygame.draw.rect(
        screen, 
        settings.SNAKE_COLOR, 
        (
            grid_offset_x + snake_row * cell_size + 1, 
            grid_offset_y + snake_col * cell_size + 1, 
            cell_size - 2, 
            cell_size - 2
        )
    )
    
    if food_pos != snake_head:
        pygame.draw.rect(
            screen,
            settings.FOOD_COLOR,
            (
                grid_offset_x + food_row * cell_size + 1,
                grid_offset_y + food_col * cell_size + 1,
                cell_size - 2,
                cell_size - 2
            )
        )
    else:
        score += 1
        food_pos = generate_food(grid_size, snake)
        print(score)
                
    move_timer += dt
    
    if move_timer >= 0.4:
        
        move_timer = 0
                
        if direction == "UP":
            snake_head[1] -= 1
        elif direction == "DOWN":
            snake_head[1] += 1
        elif direction == "LEFT":
            snake_head[0] -= 1
        elif direction == "RIGHT":
            snake_head[0] += 1
        
    if (
        snake_head[0] < 0 
        or snake_head[0] >= grid_size 
        or snake_head[1] < 0 
        or snake_head[1] >= grid_size
    ):
        running = False
    
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()
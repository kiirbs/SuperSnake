import pygame
import random

import settings
import food
import snake
from collections import deque

# Setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
move_timer = 0
score = 0
grow = False


width = screen.get_width()
height = screen.get_height()

# Grid
grid_size = settings.DEFAULT_GRID_SIZE
cell_size = min(width, height) // grid_size

# Snake
ingame_snake = snake.generate_snake(grid_size)
head = ingame_snake[0]
direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
next_direction = direction

# Food
food_pos = food.generate_food(grid_size, ingame_snake)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and direction != "DOWN":
                next_direction = "UP"
            
            elif event.key == pygame.K_s and direction != "UP":
                next_direction = "DOWN"
                
            elif event.key == pygame.K_q and direction != "RIGHT":
                next_direction = "LEFT"
                
            elif event.key == pygame.K_d and direction != "LEFT":
                next_direction = "RIGHT"
            
    screen.fill(settings.BACKGROUND_COLOR)
    
    grid_offset_x = (width - grid_size * cell_size) / 2
    grid_offset_y = (height - grid_size * cell_size) / 2

    for row in range(grid_size):
        for col in range(grid_size):
            
            x = grid_offset_x + col * cell_size
            y = grid_offset_y + row * cell_size
            
            pygame.draw.rect(screen, settings.GRID_COLOR, (x, y, cell_size, cell_size), 1)
            
    move_timer += dt
    
    head = ingame_snake[0]
    if food_pos != head:
        food.draw_food(screen, food_pos, grid_offset_x, grid_offset_y, cell_size)
        if move_timer >= 0.3:
            move_timer = 0
            direction = next_direction
            ingame_snake, grow = snake.add_snake_case(direction, ingame_snake, grow)
            head = ingame_snake[0]

    else:
        score += 1
        grow = True
        food_pos = food.generate_food(grid_size, ingame_snake)
        if move_timer >= 0.3:
            move_timer = 0
            direction = next_direction
            ingame_snake, grow = snake.add_snake_case(direction, ingame_snake, grow)
            head = ingame_snake[0]

        print(score)
        
    if (
        head[0] < 0 
        or head[0] >= grid_size 
        or head[1] < 0 
        or head[1] >= grid_size
    ):
        running = False
        
    head = ingame_snake[0]

    if head in list(ingame_snake)[1:]:
        running = False
        
    for snake_case in ingame_snake:
        snake.draw_snake(screen, snake_case, grid_offset_x, grid_offset_y, cell_size)
    
    pygame.display.flip()
    
    dt = clock.tick(settings.FPS) / 1000

pygame.quit()
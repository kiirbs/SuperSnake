import random
import pygame
from collections import deque

import settings

def generate_snake(grid_size):
    return deque([[
        random.randint(3, grid_size - 4), 
        random.randint(3, grid_size - 4)
    ]])
    
def draw_snake(screen, snake, grid_offset_x, grid_offset_y, cell_size):
    
    snake_row = snake[0]
    snake_col = snake[1]
            
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
    
def add_snake_case(direction, snake, grow):
    
    if direction == "UP":
        snake.appendleft([snake[0][0], snake[0][1] - 1])
    elif direction == "DOWN":
        snake.appendleft([snake[0][0], snake[0][1] + 1])
    elif direction == "LEFT":
        snake.appendleft([snake[0][0] - 1, snake[0][1]])
    elif direction == "RIGHT":
        snake.appendleft([snake[0][0] + 1, snake[0][1]])
        
    if not grow:
        snake.pop()
    else:
        grow = False
        
    return snake, grow
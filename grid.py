import pygame
import random

import settings

def draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y):
    for row in range(grid_size):
        for col in range(grid_size):
            
            x = grid_offset_x + col * cell_size
            y = grid_offset_y + row * cell_size
            
            pygame.draw.rect(
                screen, 
                settings.GRID_COLOR, 
                (x, y, cell_size, cell_size), 
                1
            )
            
def generate_obstacles(grid_size, snake, food_pos, obstacles_pos, head): # Creer des lignes d'obstacle ? Peut etre avec random ?
    
    possible_obstacles_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if [i, j] not in snake and [i, j] not in food_pos and [i, j] not in obstacles_pos and [i, j] != head
    ]
    
    if not possible_obstacles_pos:
        return None
    
    return random.choice(possible_obstacles_pos)

def draw_obstacles(screen, obstacles_pos, grid_offset_x, grid_offset_y, cell_size):
    
    obstacles_row = obstacles_pos[0]
    obstacles_col = obstacles_pos[1]
    
    pygame.draw.rect(
            screen,
            settings.OBSTACLES_COLOR,
            (
                grid_offset_x + obstacles_row * cell_size + 1,
                grid_offset_y + obstacles_col * cell_size + 1,
                cell_size - 2,
                cell_size - 2
            )
        )
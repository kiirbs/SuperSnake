import pygame
import random

import settings

def generate_food(grid_size, snake, food_pos, head): # Plusieurs food ? En fonction des cases restantes ?
    
    possible_food_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if [i, j] not in snake and [i, j] not in food_pos and [i, j] != head
    ]
    
    if not possible_food_pos:
        return None
    
    return random.choice(possible_food_pos)

def draw_food(screen, food_pos, grid_offset_x, grid_offset_y, cell_size):
    
    food_row = food_pos[0]
    food_col = food_pos[1]
    
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
import pygame
import random

import settings

def generate_food(grid_size, snake, food_pos, obstacles_pos, head):
    
    possible_food_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if [i, j] not in snake and [i, j] not in food_pos and [i, j] not in obstacles_pos and [i, j] != head
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
    
def generate_powerup(grid_size, snake, food_pos, powerup_pos, obstacles_pos, head):
    
    possible_effect = ["POISON", "SPEED", "SCORE", "BONUS"]
    
    possible_powerup_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if ([i, j] not in snake 
            and [i, j] not in food_pos 
            and [i, j] not in obstacles_pos 
            and [i, j] not in powerup_pos 
            and [i, j] != head
        )
    ]
    
    if not possible_powerup_pos:
        return None
    
    powerup = {
        "pos": random.choice(possible_powerup_pos),
        "type": random.choice(possible_effect)
    }
    
    return powerup

def draw_powerup(screen, pos, type, grid_offset_x, grid_offset_y, cell_size):

    row = pos[0]
    col = pos[1]
    
    if type == "POISON":
        color = settings.POISON_COLOR
    if type == "SPEED":
        color = settings.SPEED_COLOR
    if type == "SCORE":
        color = settings.SCORE_UP_COLOR
    if type == "BONUS":
        color = settings.BONUS_COLOR
    
    pygame.draw.rect(
            screen,
            color,
            (
                grid_offset_x + row * cell_size + 1,
                grid_offset_y + col * cell_size + 1,
                cell_size - 2,
                cell_size - 2
            )
        )
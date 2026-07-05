import pygame
import random

import assets
import settings

def draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y):
    for row in range(grid_size):
        for col in range(grid_size):
            
            x = grid_offset_x + col * cell_size
            y = grid_offset_y + row * cell_size
            
            sprite = assets.get_sprite(
                assets.FLOOR,
                cell_size
            )
    
            screen.blit(
                sprite,
                (
                    x,
                    y
                )
            )
            
def generate_obstacles(grid_size, food_pos, obstacles_pos, players): # Creer des lignes d'obstacle ? Peut etre avec random ?
    
    possible_obstacles_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if not any(
            [i, j] in p["snake"]
            for p in players
        )
        and [i, j] not in food_pos 
        and [i, j] not in obstacles_pos
    ]
    
    if not possible_obstacles_pos:
        return None
    
    return random.choice(possible_obstacles_pos)

def draw_obstacles(screen, obstacles_pos, grid_offset_x, grid_offset_y, cell_size):
    
    obstacles_row = obstacles_pos[0]
    obstacles_col = obstacles_pos[1]
    
    sprite = assets.get_sprite(
        assets.OBSTACLE,
        cell_size
    )
    
    screen.blit(
        sprite,
        (
            grid_offset_x + obstacles_row * cell_size,
            grid_offset_y + obstacles_col * cell_size
        )
    )
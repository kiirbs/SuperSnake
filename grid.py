import pygame
import random

import assets
import settings

def draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y):
    for row in range(grid_size):
        for col in range(grid_size):
            
            x = grid_offset_x + col * cell_size
            y = grid_offset_y + row * cell_size
            
            assets.print_asset(screen, assets.FLOOR, cell_size, x, y)
            
def draw_set(screen, grid_size, cell_size, grid_offset_x, grid_offset_y):
    
    grid_offset_x -= cell_size
    grid_offset_y -= cell_size
    
    set_size = grid_size + 2
        
    for row in range(set_size):
        for col in range(set_size):
            
            x = grid_offset_x + col * cell_size
            y = grid_offset_y + row * cell_size
            
            if row == 0 and col == 0:
                assets.print_asset(screen, assets.SET_UP_LEFT, cell_size, x, y)
                
            elif row == 0 and col != 0 and col != set_size - 1:
                assets.print_asset(screen, assets.SET_UP, cell_size, x, y)
            
            elif row == 0 and col == set_size - 1:
                assets.print_asset(screen, assets.SET_UP_RIGHT, cell_size, x, y)
                
            elif col == 0 and row != 0 and row != set_size - 1:
                assets.print_asset(screen, assets.SET_LEFT, cell_size, x, y)
                
            elif col == set_size - 1 and row != 0 and row != set_size - 1:
                assets.print_asset(screen, assets.SET_RIGHT, cell_size, x, y)
                
            elif row == set_size - 1 and col == 0:
                assets.print_asset(screen, assets.SET_DOWN_LEFT, cell_size, x, y)
                
            elif row == set_size - 1 and col != 0 and col != set_size - 1:
                assets.print_asset(screen, assets.SET_DOWN, cell_size, x, y)
                
            elif row == set_size - 1 and col == set_size - 1:
                assets.print_asset(screen, assets.SET_DOWN_RIGHT, cell_size, x, y)
            
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
    
    x = grid_offset_x + obstacles_row * cell_size
    y = grid_offset_y + obstacles_col * cell_size
    
    assets.print_asset(screen, assets.OBSTACLE, cell_size, x, y)
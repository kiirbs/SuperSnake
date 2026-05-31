import pygame

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
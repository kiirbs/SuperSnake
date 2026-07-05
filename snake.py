import random
from collections import deque

import assets

BODY_ASSETS = {
    ((0, 1), (0, 1)): "BODY_UP",
    ((0, -1), (0, -1)): "BODY_DOWN",
    ((1, 0), (1, 0)): "BODY_LEFT",
    ((-1, 0), (-1, 0)): "BODY_RIGHT",

    ((0, -1), (1, 0)): "BODY_L_LEFT",
    ((0, -1), (-1, 0)): "BODY_R_RIGHT",
    ((1, 0), (0, 1)): "BODY_L_UP",
    ((1, 0), (0, -1)): "BODY_R_DOWN",
    ((0, 1), (-1, 0)): "BODY_L_RIGHT",
    ((0, 1), (1, 0)): "BODY_R_LEFT",
    ((-1, 0), (0, -1)): "BODY_L_DOWN",
    ((-1, 0), (0, 1)): "BODY_R_UP",
}

def generate_snake(grid_size):
    return deque([[
        random.randint(3, grid_size - 4), 
        random.randint(3, grid_size - 4)
    ]])
    
def get_head_asset(direction):
    return {
        "UP": assets.HEAD_UP,
        "RIGHT": assets.HEAD_RIGHT,
        "DOWN": assets.HEAD_DOWN,
        "LEFT": assets.HEAD_LEFT
    }[direction]
    
def get_tail_asset(prev_pos, curr_pos):
    
    dx = curr_pos[0] - prev_pos[0]
    dy = curr_pos[1] - prev_pos[1]
    
    if dx == -1: return assets.TAIL_RIGHT
    if dx == 1: return assets.TAIL_LEFT
    if dy == -1: return assets.TAIL_DOWN
    if dy == 1: return assets.TAIL_UP
    
def get_body_asset(prev_pos, curr_pos, next_pos):
    
    d_in = (curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1])
    d_out = (next_pos[0] - curr_pos[0], next_pos[1] - curr_pos[1])
    
    asset_name = BODY_ASSETS.get((d_in, d_out), "BODY_RIGHT")
    return getattr(assets, asset_name)
    
def draw_snake(screen, player, grid_offset_x, grid_offset_y, cell_size):
    
    snake = player["snake"]
    n = len(snake)
    
    for i, case in enumerate(snake):
        
        prev_case = snake[i-1] if i > 0 else None
        next_case = snake[i+1] if i < n-1 else None
    
        if i == 0:
            asset = get_head_asset(player["direction"])
        
        elif i == n-1:
            asset = get_tail_asset(prev_case, case)
            
        else: 
            asset = get_body_asset(prev_case, case, next_case)
            
        sprite = assets.get_sprite(asset, cell_size)
        screen.blit(sprite, ((
            grid_offset_x + case[0] * cell_size, 
            grid_offset_y + case[1] * cell_size
        )))
    
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
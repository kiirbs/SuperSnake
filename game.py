import random

import snake
import food

def new_game(grid_size):
    
    # Snake
    ingame_snake = snake.generate_snake(grid_size)
    head = ingame_snake[0]
    direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
    next_direction = direction
    grow = False
    
    # Food
    food_pos = food.generate_food(grid_size, ingame_snake)
    
    # Score
    score = 0
    
    # Auto-move
    move_timer = 0
    
    return ingame_snake, head, direction, next_direction, grow, food_pos, score, move_timer

def turn(next_direction, ingame_snake, grow):
    
    direction = next_direction
    
    ingame_snake, grow = snake.add_snake_case(
        direction, 
        ingame_snake, 
        grow
    
    )
    head = ingame_snake[0]
            
    return direction, ingame_snake, grow, head

def grid_out_check(head, grid_size, running):
    if (
        head[0] < 0 
        or head[0] >= grid_size 
        or head[1] < 0 
        or head[1] >= grid_size
    ):
        running = False
        
    return running

def eat_que_check(ingame_snake, head, running):
    
    head = ingame_snake[0]

    if head in list(ingame_snake)[1:]:
        running = False
        
    return running
            
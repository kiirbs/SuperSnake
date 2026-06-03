import random

import snake
import food
import settings

def free_case_check(grid_size, ingame_snake, max_food, head):
    
    grid_len = grid_size ** 2
    
    snake_len = 0
    for _ in ingame_snake:
        snake_len += 1
        
    if head not in ingame_snake:
        snake_len += 1
        
    return grid_len - snake_len - max_food

def new_game(grid_size, max_food, food_interval, difficulty):
    
    # Snake
    ingame_snake = snake.generate_snake(grid_size)
    head = ingame_snake[0]
    direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
    next_direction = direction
    grow = False
    
    # Food
    food_pos = []
    for _ in range(max_food):
        food_pos.append(food.generate_food(grid_size, ingame_snake, food_pos, head))
        
    food_interval = (max_food - 1) * difficulty["food_interval"]
        
    # Score
    score = 0
    
    # Auto-move
    move_timer = 0
    
    # Free Cases
    free_cases = free_case_check(grid_size, ingame_snake, max_food, head)
    
    return ingame_snake, head, direction, next_direction, grow, food_pos, score, move_timer, free_cases, food_interval

def turn(next_direction, ingame_snake, grow):
    
    direction = next_direction
    
    ingame_snake, grow = snake.add_snake_case(
        direction, 
        ingame_snake, 
        grow
    
    )
    head = ingame_snake[0]
            
    return direction, ingame_snake, grow, head

def grid_out_check(head, grid_size, ingame_snake):
    
    head = ingame_snake[0]
    
    if (
        head[0] < 0 
        or head[0] >= grid_size 
        or head[1] < 0 
        or head[1] >= grid_size
    ):
        return True
    
    return False

def eat_que_check(ingame_snake, head):
    
    head = ingame_snake[0]

    if head in list(ingame_snake)[1:]:
        return True
    
    return False

def game_setup(difficulty):
    
    selected_grid_size = difficulty["grid_size"]
    move_interval = difficulty["move_interval"]
    max_food = difficulty["max_food"]
    food_interval = difficulty["food_interval"]
    game_state = "GAME"
    
    return selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty
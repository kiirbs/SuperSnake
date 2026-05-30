import random

def generate_food(grid_size, snake):
    
    possible_food_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if [i, j] not in snake
    ]
    
    return random.choice(possible_food_pos)
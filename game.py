import random
import pygame

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

def draw_score(screen, score, best_score, width, height):
    
    dw = width / settings.DEFAULT_WIDTH
    dh = height / settings.DEFAULT_HEIGHT
    
    score_width = max(25, int(settings.DEFAULT_BUTTON_WIDTH / 2.5 * dw))
    score_height = max(6, int(settings.DEFAULT_BUTTON_HEIGHT / 2.5 * dh))
    
    base_font_size = max(3, int(settings.DEFAULT_SCORE_FONT * dh))
    score_font = pygame.font.Font(None, base_font_size)
    
    score_rect = pygame.Rect(
        int(40 * dw), 
        int((30 * dh) + score_height),
        score_width,
        score_height
    )
    
    best_score_rect = pygame.Rect(
        int(40 * dw), 
        int(20 * dh),
        score_width,
        score_height
    )
    
    score_text_surface = score_font.render(
        f"SCORE : {score}",
        True,
        settings.TEXT_COLOR
    )
    
    best_score_text_surface = score_font.render(
        f"BEST : {best_score}",
        True,
        settings.TEXT_COLOR
    )
        
    pygame.draw.rect(
        screen,
        settings.SCORE_COLOR,
        score_rect,
    )
    
    pygame.draw.rect(
        screen,
        settings.SCORE_COLOR,
        best_score_rect,
    )
        
    score_text_rect = score_text_surface.get_rect(
        center=score_rect.center
    )
    
    best_score_text_rect = best_score_text_surface.get_rect(
        center=best_score_rect.center
    )
        
    screen.blit(score_text_surface, score_text_rect)
    
    screen.blit(best_score_text_surface, best_score_text_rect)
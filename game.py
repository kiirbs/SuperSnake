import random
import pygame

import snake
import food
import settings
import menu
import grid

def cell_size_check(selected_grid_size, width, height):
    
    grid_size = selected_grid_size
    cell_size = min(width, height - 150) // grid_size
    
    return grid_size, cell_size

def offsetts_check(width, height, grid_size, cell_size):
    
    grid_offset_x = (width - grid_size * cell_size) / 2
    grid_offset_y = 100 + (((height - 150) - grid_size * cell_size) / 2)
    
    return grid_offset_x, grid_offset_y

def free_case_check(grid_size, ingame_snake, max_food, head):
    
    grid_len = grid_size ** 2
    
    snake_len = 0
    for _ in ingame_snake:
        snake_len += 1
        
    if head not in ingame_snake:
        snake_len += 1
        
    return grid_len - snake_len - max_food

def speed_adjustment(score, speed_limit, move_interval):
    
    while score >= speed_limit:
        move_interval *= 0.98
        speed_limit += 5
        
    return move_interval, speed_limit

def new_game(grid_size, max_food, food_interval, difficulty):
    
    # Snake
    ingame_snake = snake.generate_snake(grid_size)
    head = ingame_snake[0]
    direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
    next_direction = direction
    grow = False
    
    # Obstacles
    obstacles_pos = []
    
    # Power Up
    powerup_pos = []
    
    # Food
    food_pos = []
    for _ in range(max_food):
        food_pos.append(food.generate_food(grid_size, ingame_snake, food_pos, obstacles_pos, head))
        
    food_interval = (max_food - 1) * difficulty["food_interval"]
        
    # Score
    score = 0
    speed_limit = 5
    
    # Auto-move
    move_timer = 0
    
    # Free Cases
    free_cases = free_case_check(grid_size, ingame_snake, max_food, head)
    
    return ingame_snake, head, direction, next_direction, grow, food_pos, score, speed_limit, move_timer, free_cases, food_interval, obstacles_pos, powerup_pos

def new_extra_game(grid_size, ingame_snake, food_pos, head, max_obstacles, max_powerup, difficulty):
    
    powerup_pos = []
    obstacles_pos = []
    
    max_obstacle_len = grid_size // 4
    possible_direction = ["UP", "LEFT", "DOWN", "RIGHT"]
    
    for _ in range(max_obstacles):
        
        obstacle_len = random.randint(1, max_obstacle_len)
        obstacle = grid.generate_obstacles(grid_size, ingame_snake, food_pos, obstacles_pos, head)
        obstacles_pos.append(obstacle)
        direction = random.choice(possible_direction)
        
        for _ in range(obstacle_len):
            
            if direction == "UP":
                next_obstacle = [obstacle[0], obstacle[1] - 1]
            if direction == "LEFT":
                next_obstacle = [obstacle[0] - 1, obstacle[1]]
            if direction == "DOWN":
                next_obstacle = [obstacle[0], obstacle[1] + 1]
            if direction == "RIGHT":
                next_obstacle = [obstacle[0] + 1, obstacle[1]]
                
            if (next_obstacle[0] < 0 
                or next_obstacle[0] >= grid_size 
                or next_obstacle[1] < 0 
                or next_obstacle[1] >= grid_size
                or next_obstacle in ingame_snake 
                or next_obstacle in food_pos 
                or next_obstacle in powerup_pos 
                or next_obstacle in obstacles_pos
                or next_obstacle == head
            ):
                break
            
            obstacle = next_obstacle
            obstacles_pos.append(obstacle)
            
    for _ in range(max_powerup):
        powerup_pos.append(food.generate_powerup(
            grid_size, 
            ingame_snake, 
            food_pos, 
            powerup_pos, 
            obstacles_pos, 
            head
        ))
                
    powerup_interval = (max_powerup - 1) * difficulty["power_up_interval"] if max_powerup > 1 else 1
    
    return obstacles_pos, powerup_pos, powerup_interval

def turn(next_direction, ingame_snake, grow):
    
    direction = next_direction
    
    ingame_snake, grow = snake.add_snake_case(
        direction, 
        ingame_snake, 
        grow
    
    )
    head = ingame_snake[0]
            
    return direction, ingame_snake, grow, head

def reset_powerup(head, ingame_snake, food_pos, powerup_pos, powerup_interval, obstacles_pos, grid_size, difficulty, free_cases, max_powerup):
    
    # Generate Powerup
    for i, item in enumerate(powerup_pos):
        if item["pos"] == head:
            powerup_pos[i] = food.generate_powerup(
                grid_size, 
                ingame_snake,
                food_pos,
                powerup_pos,
                obstacles_pos,
                head
            )
                        
    # Powerup Downgrade
    if free_cases <= powerup_interval:
        max_powerup -= 1
        powerup_interval = (max_powerup - 1) * difficulty["power_up_interval"] if max_powerup > 1 else 1
        powerup_pos.pop()
        
    return powerup_pos, max_powerup, powerup_interval

def grid_out_check(head, grid_size):
    
    if (
        head[0] < 0 
        or head[0] >= grid_size 
        or head[1] < 0 
        or head[1] >= grid_size
    ):
        return True
    
    return False

def eat_que_check(ingame_snake, head):

    if head in list(ingame_snake)[1:]:
        return True
    
    return False

def hit_obstacles_check(head, obstacles_pos):
    
    if head in obstacles_pos:
        return True
    
    return False

def game_setup(difficulty):
    
    selected_grid_size = difficulty["grid_size"]
    move_interval = difficulty["move_interval"]
    max_food = difficulty["max_food"]
    food_interval = difficulty["food_interval"]
    game_state = "GAME"
    
    return selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty

def extra_game_setup(difficulty):
    
    max_obstacles = difficulty["max_obstacles"]
    max_powerup = difficulty["max_power_up"]
    powerup_interval = difficulty["power_up_interval"]
    
    return max_obstacles, max_powerup, powerup_interval

def create_rect(x, y, width, height):
    
    rect = pygame.Rect(
            x, 
            y,
            width, 
            height
        )
    
    return rect

def create_text(font, text, color, rect):
    
    text_surface = font.render(
        text,
        True,
        color
    )
    
    text_rect = text_surface.get_rect(
        center=rect.center
    )
    
    return text_surface, text_rect

def draw_score(screen, score, best_score, width, height):
    
    dw, dh = menu.get_scale(width, height)
    
    score_width = max(settings.DEFAULT_SCORE_MIN_WIDTH, int(settings.DEFAULT_SCORE_WIDTH * dw))
    score_height = max(settings.DEFAULT_SCORE_MIN_HEIGHT, int(settings.DEFAULT_SCORE_HEIGHT * dh))
    
    base_font_size = max(3, int(settings.DEFAULT_SCORE_FONT * dh))
    score_font = pygame.font.Font(None, base_font_size)
    
    score_rect = create_rect(int(40 * dw), int((30 * dh) + score_height), score_width, score_height)
    best_score_rect = create_rect(int(40 * dw), int(20 * dh), score_width, score_height)
        
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
    
    score_text_surface, score_text_rect = create_text(
        score_font, 
        f"SCORE : {score}", 
        settings.TEXT_COLOR, 
        score_rect
    )
    best_score_text_surface, best_score_text_rect = create_text(
        score_font, 
        f"BEST : {best_score}", 
        settings.TEXT_COLOR, 
        best_score_rect
    )
        
    screen.blit(score_text_surface, score_text_rect)
    screen.blit(best_score_text_surface, best_score_text_rect)
import pygame
from collections import deque

import settings
import food
import snake
import game
import grid
import menu
import save
import audio

# Pygame Setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(
    (settings.DEFAULT_WIDTH, settings.DEFAULT_HEIGHT),
    pygame.RESIZABLE
)
clock = pygame.time.Clock()
running = True
dt = 0

# Setup
game_state = "MENU"
mode = "SOLO"
extra_mode = False
best_score = 0
difficulty = settings.NORMAL
difficulty_name = difficulty["name"]
move_interval = difficulty["move_interval"]
direction = None
max_obstacles = difficulty["max_obstacles"]
max_powerup = difficulty["max_power_up"]
powerup_interval = difficulty["power_up_interval"]
highscores = save.load_highscores()

speed_end_timer = 0
bonus_grow = False

width = screen.get_width()
height = screen.get_height()

# Menu
buttons = deque([])
buttons = menu.draw_menu(screen, width, height, settings.MENU)

# Grid
selected_grid_size = difficulty["grid_size"]
grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)

# Food
max_food = difficulty["max_food"]
food_interval = difficulty["food_interval"]

while running:
    for event in pygame.event.get():    # Check Event
        if event.type == pygame.QUIT:   # Quit
            running = False
            
        elif event.type == pygame.KEYDOWN:  # ZQSD Check + ULDR Check + SPACE Check
            if (event.key == pygame.K_z or event.key == pygame.K_UP) and direction != "DOWN" and game_state != "PAUSE":
                next_direction = "UP"
            
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and direction != "UP" and game_state != "PAUSE":
                next_direction = "DOWN"
                
            elif (event.key == pygame.K_q or event.key == pygame.K_LEFT) and direction != "RIGHT" and game_state != "PAUSE":
                next_direction = "LEFT"
                
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and direction != "LEFT" and game_state != "PAUSE":
                next_direction = "RIGHT"
                
            elif event.key == pygame.K_SPACE and (game_state == "GAME" or game_state == "PAUSE"):
                game_state = "PAUSE" if game_state == "GAME" else "GAME"
                
        elif event.type == pygame.VIDEORESIZE:  # Screen Resize
            
            width = event.w
            height = event.h
            
            cell_size = min(width, height - 150) // grid_size
            
        elif event.type == pygame.MOUSEBUTTONDOWN: # Clics
            for value, button in buttons:
                if button.collidepoint(event.pos):
                    audio.CLICK_SOUND.play()
                    if value == "SOLO":
                        mode = "SOLO"
                        game_state = "MENU2"
                        
                    elif value == "ONE-BOARD MULTI":
                        mode = "MULTI1"
                        game_state = "MENU2"
                        
                    elif value == "TWO-BOARD MULTI":
                        mode = "MULTI2"
                        game_state = "MENU2"
                        
                    elif value == "EASY":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(settings.EASY)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.EASY)
                        
                    elif value == "NORMAL":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(settings.NORMAL)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.NORMAL)
                        
                    elif value == "HARD":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(settings.HARD)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.HARD)
                        
                    elif value == "ULTRA HARD":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(settings.ULTRA_HARD)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.ULTRA_HARD)
                        
                    elif value == "TRY AGAIN":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(difficulty)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(difficulty)
                        
                    elif value == "RETURN TO MENU" or value == "RETURN":
                        game_state = "MENU"
                        best_score = 0
                        
                    elif value == "EXTRA":
                        extra_mode = True if extra_mode == False else False
                    
                    # New Game
                    grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)                   
                    ingame_snake, head, direction, next_direction, grow, food_pos, score, speed_limit, move_timer, free_cases, food_interval, obstacles_pos, powerup_pos = game.new_game(
                        selected_grid_size, 
                        max_food, 
                        food_interval,
                        difficulty
                    )
                    difficulty_name = difficulty["name"]
                    old_move_interval = 0
                    speed_end_timer = 0
                    bonus_grow = False
                    bonus_timer = 0
                    if extra_mode:
                        obstacles_pos, powerup_pos, powerup_interval = game.new_extra_game(
                            grid_size, 
                            ingame_snake, 
                            food_pos, 
                            head,
                            max_obstacles, 
                            max_powerup, 
                            difficulty
                        )

    # Principal Menu
    if game_state == "MENU":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Draw Difficulty Menu
        buttons = menu.draw_menu(screen, width, height, settings.MENU)
        
        # Grid Size and Cell Size Check
        grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
    
    # Difficulty Menu
    elif game_state == "MENU2":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Draw Difficulty Menu   
        buttons = menu.draw_menu(screen, width, height, settings.DIFFICULT)
        buttons = menu.draw_second_menu(screen, buttons, extra_mode, width, height, settings.DIFFICULT)
        
        # Grid Size and Cell Size Check
        grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
    
    # In Game
    elif game_state == "GAME":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
    
        # Offsets
        grid_offset_x, grid_offset_y = game.offsetts_check(width, height, grid_size, cell_size)

        # Draw Grid
        grid.draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y)
        
        # Moving Interval
        move_timer += dt
        head = ingame_snake[0]
        
        if speed_end_timer > 0:
            speed_end_timer -= dt
            
            if speed_end_timer <= 0:
                move_interval = old_move_interval

        # Turn
        if move_timer >= move_interval:
            move_timer = 0
            
            if bonus_grow:
                grow = True
                bonus_timer -= 1
                
                if bonus_timer <= 0:
                    bonus_grow = False
                    
            direction, ingame_snake, grow, head = game.turn(
                next_direction,
                ingame_snake,
                grow
            )

            # Eat food
            if head in food_pos:
                score += 1
                grow = True
                free_cases = game.free_case_check(grid_size, ingame_snake, max_food, head)
                move_interval, old_move_interval, speed_limit = game.speed_adjustment(score, speed_limit, move_interval, old_move_interval)
                audio.FOOD_SOUND.play()
                
                # Generate Food
                for i, item in enumerate(food_pos):
                    if item == head:
                        food_pos[i] = food.generate_food(
                            grid_size, 
                            ingame_snake,
                            food_pos,
                            obstacles_pos,
                            head
                        )
                        
                # Food Downgrade
                if free_cases <= food_interval:
                    max_food -= 1
                    food_interval = (max_food - 1) * difficulty["food_interval"]
                    food_pos.pop()
                    
                    if free_cases <= 0:
                        game_state = "WIN"
                        audio.WIN_SOUND.play()
            
            # Eat Power Up
            for powerup in powerup_pos:
                
                if powerup is None:
                    continue
                    
                if head == powerup["pos"]:
                    free_cases = game.free_case_check(grid_size, ingame_snake, max_food, head)
                    
                    if powerup["type"] == "POISON":
                        score -= 1
                        ingame_snake.pop()
                        audio.POISON_SOUND.play()
                        
                        if len(ingame_snake) <= 0 or score < 0:
                            game_state = "GAME_OVER"
                            audio.LOSE_SOUND.play()
                            
                        powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                            head, 
                            ingame_snake, 
                            food_pos, 
                            powerup_pos,
                            powerup_interval, 
                            obstacles_pos, 
                            grid_size, 
                            difficulty, 
                            free_cases, 
                            max_powerup
                        )
                            
                    elif powerup["type"] == "SPEED":
                        score += 1
                        grow = True
                        audio.POWERUP_SOUND.play()
                        
                        if speed_end_timer <= 0:
                            old_move_interval = move_interval
                            move_interval *= 0.75
                            speed_end_timer = 5
                        else:
                            speed_end_timer = 5
                        
                        move_interval, old_move_interval, speed_limit = game.speed_adjustment(score, speed_limit, move_interval, old_move_interval)
                        powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                            head, 
                            ingame_snake, 
                            food_pos, 
                            powerup_pos, 
                            powerup_interval,
                            obstacles_pos, 
                            grid_size, 
                            difficulty, 
                            free_cases, 
                            max_powerup
                        )       
                        
                    elif powerup["type"] == "SCORE":
                        score += 5
                        grow = True
                        audio.POWERUP_SOUND.play()
                        
                        move_interval, old_move_interval, speed_limit = game.speed_adjustment(score, speed_limit, move_interval, old_move_interval)
                        powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                            head, 
                            ingame_snake, 
                            food_pos, 
                            powerup_pos, 
                            powerup_interval,
                            obstacles_pos, 
                            grid_size, 
                            difficulty, 
                            free_cases, 
                            max_powerup
                        )
                        
                    elif powerup["type"] == "BONUS":
                        score += 1
                        grow = True
                        bonus_grow = True
                        bonus_timer = 5
                        audio.POWERUP_SOUND.play()
                        
                        move_interval, old_move_interval, speed_limit = game.speed_adjustment(score, speed_limit, move_interval, old_move_interval)
                        powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                            head, 
                            ingame_snake, 
                            food_pos, 
                            powerup_pos, 
                            powerup_interval,
                            obstacles_pos, 
                            grid_size, 
                            difficulty, 
                            free_cases, 
                            max_powerup
                        )
        
        # Best Score
        
        mode2 = "EXTRA" if extra_mode else "CLASSIC"
        
        if score > highscores[mode2][difficulty_name]:
            highscores[mode2][difficulty_name] = score
        
        best_score = highscores[mode2][difficulty_name]
        
        # Speed & Len  
        speed = round(1 / move_interval, 1)
        snake_len = len(ingame_snake)
        
        # Draw Score & Speed & Len
        game.draw_score(screen, score, best_score, speed, snake_len, width, height)
        
        if len(ingame_snake) > 0:
            head = ingame_snake[0]
    
        # Grid-Out Check
        if game.grid_out_check(head, grid_size):
            game_state = "GAME_OVER"
            audio.LOSE_SOUND.play()
        
        # Que-Eating Check
        if game.eat_que_check(ingame_snake, head):
            game_state = "GAME_OVER"
            audio.LOSE_SOUND.play()
        
        # Hit-Obstacles Check
        if extra_mode:
            if game.hit_obstacles_check(head, obstacles_pos):
                game_state = "GAME_OVER"
                audio.LOSE_SOUND.play()

        # Draw Food
        for item in food_pos:
            food.draw_food(screen, item, grid_offset_x, grid_offset_y, cell_size)

        # Draw Snake
        for snake_case in ingame_snake:
            if (
                head[0] >= 0 
                and head[0] < grid_size 
                and head[1] >= 0 
                and head[1] < grid_size
            ):
                snake.draw_snake(screen, snake_case, grid_offset_x, grid_offset_y, cell_size)
                
        if extra_mode:
            
            # Draw Obstacles
            for item in obstacles_pos:
                
                grid.draw_obstacles(screen, item, grid_offset_x, grid_offset_y, cell_size)
                
            # Draw Power Up
            for powerup in powerup_pos:
                
                if powerup is None:
                    continue
                
                food.draw_powerup(screen, powerup["pos"], powerup["type"], grid_offset_x, grid_offset_y, cell_size)
    
    # Pause
    elif game_state == "PAUSE":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Offsets
        grid_offset_x, grid_offset_y = game.offsetts_check(width, height, grid_size, cell_size)
        
        # Draw Grid
        grid.draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y)
        
        # Draw Food
        for item in food_pos:
            food.draw_food(screen, item, grid_offset_x, grid_offset_y, cell_size)
        
        # Draw Snake
        for snake_case in ingame_snake:
            snake.draw_snake(screen, snake_case, grid_offset_x, grid_offset_y, cell_size)
        
        if extra_mode:
            
            # Draw Obstacles
            for item in obstacles_pos:
                grid.draw_obstacles(screen, item, grid_offset_x, grid_offset_y, cell_size)
                
            # Draw Power Up
            for powerup in powerup_pos:
                
                if powerup is None:
                    continue
                
                food.draw_powerup(screen, powerup["pos"], powerup["type"], grid_offset_x, grid_offset_y, cell_size)
                
        # Draw Score
        game.draw_score(screen, score, best_score, speed, snake_len, width, height)
        
        # Print PAUSED
        menu.print_game_result(screen, "PAUSED", width, height)
        
    elif game_state == "GAME_OVER":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        #if score > highscores[mode2][difficulty_name]:
        save.save_highscores(highscores)
        
        # Print GAME OVER
        menu.print_game_result(screen, "GAME OVER", width, height)
        
        # Draw Score
        game.draw_score(screen, score, best_score, speed, snake_len, width, height)
        
        # Buttons
        buttons = menu.draw_game_over(screen, width, height)
        
        # Grid Size and Cell Size Check
        grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
        
    elif game_state == "WIN":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        #if score > highscores[mode2][difficulty_name]:
        save.save_highscores(highscores)
        
        # Print YOU WIN
        menu.print_game_result(screen, "YOU WIN", width, height)
        
        # Draw Score
        game.draw_score(screen, score, best_score, width, height)
        
        # Buttons
        buttons = menu.draw_game_over(screen, width, height)
        
        # Grid Size and Cell Size Check
        grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
        
    # Print
    pygame.display.flip()
    
    # Clock
    dt = clock.tick(settings.FPS) / 1000

pygame.quit()
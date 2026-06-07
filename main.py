import pygame
from collections import deque

import settings
import food
import snake
import game
import grid
import menu

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode(
    (settings.DEFAULT_WIDTH, settings.DEFAULT_HEIGHT),
    pygame.RESIZABLE
)
clock = pygame.time.Clock()
running = True
dt = 0

# Setup
game_state = "MENU"
best_score = 0
difficulty = settings.NORMAL
move_interval = difficulty["move_interval"]
direction = None

width = screen.get_width()
height = screen.get_height()

# Menu
buttons = deque([])
buttons = menu.draw_menu(screen, width, height, settings.MENU)

# Grid
selected_grid_size = difficulty["grid_size"]
grid_size = selected_grid_size
cell_size = min(width, height - 150) // grid_size

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
                        
                    elif value == "NORMAL":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(settings.NORMAL)
                        
                    elif value == "HARD":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(settings.HARD)
                        
                    elif value == "ULTRA HARD":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(settings.ULTRA_HARD)
                        
                    elif value == "TRY AGAIN":
                        selected_grid_size, move_interval, max_food, food_interval, game_state, difficulty = game.game_setup(difficulty)
                        
                    elif value == "RETURN TO MENU" or value == "RETURN":
                        game_state = "MENU"
                        best_score = 0
                    
                    # New Game
                    grid_size = selected_grid_size 
                    cell_size = min(width, height - 150) // grid_size                   
                    ingame_snake, head, direction, next_direction, grow, food_pos, score, move_timer, free_cases, food_interval = game.new_game(
                        selected_grid_size, 
                        max_food, 
                        food_interval,
                        difficulty
                    )

    # Principal Menu
    if game_state == "MENU":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Draw Difficulty Menu
        buttons = menu.draw_menu(screen, width, height, settings.MENU)
        
        # Grid Size and Cell Size Check
        grid_size = selected_grid_size
        cell_size = min(width, height - 150) // grid_size
    
    # Difficulty Menu
    elif game_state == "MENU2":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Draw Difficulty Menu
        if len(buttons) > len(settings.DIFFICULT):
            buttons.pop()
            
        buttons = menu.draw_menu(screen, width, height, settings.DIFFICULT)
        buttons.appendleft(menu.draw_return(screen, width, height))
        
        # Grid Size and Cell Size Check
        grid_size = selected_grid_size
        cell_size = min(width, height - 150) // grid_size
    
    # In Game
    elif game_state == "GAME":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
    
        # Offsets
        grid_offset_x = (width - grid_size * cell_size) / 2
        grid_offset_y = 100 + (((height - 150) - grid_size * cell_size) / 2)

        # Draw Grid
        grid.draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y)
        
        # Moving Interval
        move_timer += dt
        head = ingame_snake[0]

        # Turn
        if move_timer >= move_interval:
            move_timer = 0
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
                for i, item in enumerate(food_pos):
                    if item == head:
                        food_pos[i] = food.generate_food(
                            grid_size, 
                            ingame_snake,
                            food_pos, 
                            head
                        )
                        
                # Food Downgrade
                if free_cases <= food_interval:
                    max_food -= 1
                    food_interval = (max_food - 1) * difficulty["food_interval"]
                    food_pos.pop()
                    if free_cases <= 0:
                        game_state = "WIN"
        
        # Best Score
        if score > best_score:
            best_score = score
        
        # Draw Score
        game.draw_score(screen, score, best_score, width, height)
    
        head = ingame_snake[0]
    
        # Grid-Out Check
        if game.grid_out_check(head, grid_size, ingame_snake):
            game_state = "GAME_OVER"
        
        # Que-Eating Check
        if game.eat_que_check(ingame_snake, head):
            game_state = "GAME_OVER"

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
    
    # Pause
    elif game_state == "PAUSE":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Offsets
        grid_offset_x = (width - grid_size * cell_size) / 2
        grid_offset_y = 100 + (((height - 150) - grid_size * cell_size) / 2)
        
        # Draw Grid
        grid.draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y)
        
        # Draw Food
        for item in food_pos:
            food.draw_food(screen, item, grid_offset_x, grid_offset_y, cell_size)
        
        # Draw Snake
        for snake_case in ingame_snake:
            snake.draw_snake(screen, snake_case, grid_offset_x, grid_offset_y, cell_size)
        
        # Draw Score
        game.draw_score(screen, score, best_score, width, height)
        
        # Print PAUSED
        menu.print_game_result(screen, "PAUSED", width, height)
        
    elif game_state == "GAME_OVER":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Print GAME OVER
        menu.print_game_result(screen, "GAME OVER", width, height)
        
        # Draw Score
        game.draw_score(screen, score, best_score, width, height)
        
        # Buttons
        buttons = menu.draw_game_over(screen, width, height)
        
        # Grid Size and Cell Size Check
        grid_size = selected_grid_size
        cell_size = min(width, height - 150) // grid_size
        
    elif game_state == "WIN":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Print YOU WIN
        menu.print_game_result(screen, "YOU WIN", width, height)
        
        # Draw Score
        game.draw_score(screen, score, best_score, width, height)
        
        # Buttons
        buttons = menu.draw_game_over(screen, width, height)
        
        # Grid Size and Cell Size Check
        grid_size = selected_grid_size
        cell_size = min(width, height - 150) // grid_size
        
    # Print
    pygame.display.flip()
    
    # Clock
    dt = clock.tick(settings.FPS) / 1000

pygame.quit()
import pygame

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
difficulty = settings.NORMAL
move_interval = difficulty["move_interval"]

width = screen.get_width()
height = screen.get_height()

# Menu
buttons = []
buttons = menu.draw_menu(screen, width, height)

# Grid
selected_grid_size = difficulty["grid_size"]
grid_size = selected_grid_size
cell_size = min(width, height) // grid_size

# Food
max_food = difficulty["max_food"]
food_interval = difficulty["food_interval"]

while running:
    for event in pygame.event.get():    # Check Event
        if event.type == pygame.QUIT:   # Quit
            running = False
            
        elif event.type == pygame.KEYDOWN:  # ZQSD Check
            if event.key == pygame.K_z and direction != "DOWN":
                next_direction = "UP"
            
            elif event.key == pygame.K_s and direction != "UP":
                next_direction = "DOWN"
                
            elif event.key == pygame.K_q and direction != "RIGHT":
                next_direction = "LEFT"
                
            elif event.key == pygame.K_d and direction != "LEFT":
                next_direction = "RIGHT"
                
        elif event.type == pygame.VIDEORESIZE:  # Screen Resize
            
            width = event.w
            height = event.h
            
            cell_size = min(width, height) // grid_size
            
        elif event.type == pygame.MOUSEBUTTONDOWN: # Clic
            for value, button in buttons:
                if button.collidepoint(event.pos):
                    if value == "EASY":
                        difficulty = settings.EASY
                        selected_grid_size = difficulty["grid_size"]
                        move_interval = difficulty["move_interval"]
                        max_food = difficulty["max_food"]
                        food_interval = difficulty["food_interval"]
                        
                    elif value == "NORMAL":
                        difficulty = settings.NORMAL
                        selected_grid_size = difficulty["grid_size"]
                        move_interval = difficulty["move_interval"]
                        max_food = difficulty["max_food"]
                        food_interval = difficulty["food_interval"]
                        
                    elif value == "HARD":
                        difficulty = settings.HARD
                        selected_grid_size = difficulty["grid_size"]
                        move_interval = difficulty["move_interval"]
                        max_food = difficulty["max_food"]
                        food_interval = difficulty["food_interval"]
                        
                    elif value == "ULTRA HARD":
                        difficulty = settings.ULTRA_HARD
                        selected_grid_size = difficulty["grid_size"]
                        move_interval = difficulty["move_interval"]
                        max_food = difficulty["max_food"]
                        food_interval = difficulty["food_interval"]
                            
                    grid_size = selected_grid_size 
                    cell_size = min(width, height) // grid_size                   
                    ingame_snake, head, direction, next_direction, grow, food_pos, score, move_timer, free_cases, food_interval = game.new_game(
                        selected_grid_size, 
                        max_food, 
                        food_interval,
                        difficulty
                    )
                    game_state = "GAME"

    if game_state == "MENU":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        buttons = menu.draw_menu(screen, width, height)
        
        grid_size = selected_grid_size
        cell_size = min(width, height) // grid_size
                
    elif game_state == "GAME":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
    
        # Offsets
        grid_offset_x = (width - grid_size * cell_size) / 2
        grid_offset_y = (height - grid_size * cell_size) / 2

        # Draw Grid
        grid.draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y)
            
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
                if free_cases <= food_interval:
                    max_food -= 1
                    food_interval = (max_food - 1) * difficulty["food_interval"]
                    food_pos.pop()
                    if free_cases <= 0:
                        game_state = "WIN"
                    
                print(score)
    
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

        for snake_case in ingame_snake:
            if (
                head[0] >= 0 
                and head[0] < grid_size 
                and head[1] >= 0 
                and head[1] < grid_size
            ):
                snake.draw_snake(screen, snake_case, grid_offset_x, grid_offset_y, cell_size) # Draw Snake
        
    elif game_state == "GAME_OVER":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
    elif game_state == "WIN":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
    # Print
    pygame.display.flip()
    
    # Clock
    dt = clock.tick(settings.FPS) / 1000

pygame.quit()
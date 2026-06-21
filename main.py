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
max_obstacles = difficulty["max_obstacles"]
max_powerup = difficulty["max_power_up"]
powerup_interval = difficulty["power_up_interval"]
highscores = save.load_highscores()
players = []
winner = None

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
            for p in players:
                if event.key in p["controls"]:
                    if p["controls"][event.key] == "UP" and p["direction"] != "DOWN" and game_state != "PAUSE":
                        p["next_direction"] = p["controls"][event.key]
            
                    elif p["controls"][event.key] == "DOWN" and p["direction"] != "UP" and game_state != "PAUSE":
                        p["next_direction"] = p["controls"][event.key]
                
                    elif p["controls"][event.key] == "LEFT" and p["direction"] != "RIGHT" and game_state != "PAUSE":
                        p["next_direction"] = p["controls"][event.key]
                
                    elif p["controls"][event.key] == "RIGHT" and p["direction"] != "LEFT" and game_state != "PAUSE":
                        p["next_direction"] = p["controls"][event.key]
                
            if event.key == pygame.K_SPACE and (game_state == "GAME" or game_state == "PAUSE"):
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
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.EASY)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.EASY)
                        
                    elif value == "NORMAL":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.NORMAL)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.NORMAL)
                        
                    elif value == "HARD":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.HARD)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.HARD)
                        
                    elif value == "ULTRA HARD":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.ULTRA_HARD)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(settings.ULTRA_HARD)
                        
                    elif value == "TRY AGAIN":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(difficulty)
                        if extra_mode:
                            max_obstacles, max_powerup, powerup_interval = game.extra_game_setup(difficulty)
                        
                    elif value == "RETURN TO MENU" or value == "RETURN":
                        game_state = "MENU"
                        best_score = 0
                        
                    elif value == "EXTRA":
                        extra_mode = True if extra_mode == False else False
                    
                    # New Game
                    grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
                    difficulty_name = difficulty["name"]                
                    players, food_pos, free_cases, food_interval, obstacles_pos, powerup_pos, winner = game.new_game(
                        selected_grid_size, 
                        max_food, 
                        food_interval,
                        difficulty,
                        mode
                    )
                    if extra_mode:
                        obstacles_pos, powerup_pos, powerup_interval = game.new_extra_game(
                            grid_size, 
                            food_pos, 
                            max_obstacles, 
                            max_powerup, 
                            difficulty,
                            players
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
        
        # Moving Interval
        for p in players:
            p["move_timer"] += dt
            if p["snake_len"] > 0:
                p["head"] = p["snake"][0]
            p["speed_end_timer"], p["move_interval"] = game.speed_timer(
                p["speed_end_timer"],
                p["move_interval"],
                p["old_move_interval"],
                dt
            )

        # Move
        for p in players:
            if p["snake_len"] > 0:
                game.move(p)

        # Eat food
        for p in players:
            food_pos, max_food, food_interval, game_state = food.eat_food_check(
                p,
                players,
                grid_size,
                difficulty,
                game_state,
                obstacles_pos,
                food_pos,
                max_food,
                food_interval,
                mode
            )
            
        # Eat Power Up
        for p in players:
            game_state, winner, powerup_pos, max_powerup, powerup_interval = food.eat_powerup_check(
                p, 
                players,
                grid_size, 
                difficulty, 
                game_state,
                obstacles_pos, 
                food_pos,
                max_food, 
                powerup_pos, 
                max_powerup, 
                powerup_interval,
                mode
            )
        
        # Best Score Check
        mode2 = "EXTRA" if extra_mode else "CLASSIC"
        for p in players:
            p["best_score"] = game.best_score_check(p, highscores, mode2, difficulty_name)
        
        # Speed & Len Check
        for p in players:
            p["speed"] = round(1 / p["move_interval"], 1)
            p["snake_len"] = len(p["snake"])
    
        # Grid-Out & Que-Eating & Multiplayer Collisions Check
        if mode != "SOLO":
            game_state, winner = game.hit_player_check(
                players[0]["head"], 
                players[1]["head"], 
                players[0]["snake"], 
                players[1]["snake"]
            ) 
        for p in players:
            if game.grid_out_check(p["head"], grid_size) or game.eat_que_check(p["snake"], p["head"]) or p["snake_len"] <= 0:
                if mode == "SOLO":
                    game_state = "GAME_OVER"
                    audio.LOSE_SOUND.play()
                else:
                    if p["name"] == "player_1":
                        game_state, winner = "PLAYER_WIN", "P2"
                    else:
                        game_state, winner = "PLAYER_WIN", "P1"
                    audio.WIN_SOUND.play()
        
        # Hit-Obstacles Check
        if extra_mode:
            for p in players:
                if game.hit_obstacles_check(p["head"], obstacles_pos):
                    if mode == "SOLO":
                        game_state = "GAME_OVER"
                        audio.LOSE_SOUND.play()
                    else:
                        if p["name"] == "player_1":
                            game_state, winner = "PLAYER_WIN", "P2"
                        else:
                            game_state, winner = "PLAYER_WIN", "P1"
                        audio.WIN_SOUND.play()

        # Draw Grid
        grid.draw_grid(screen, grid_size, cell_size, grid_offset_x, grid_offset_y)
        
        # Draw Score
        for p in players:
            game.draw_score(screen, p, width, height)
            if p["snake_len"] > 0:
                p["head"] = p["snake"][0]

        # Draw Food
        for item in food_pos:
            food.draw_food(screen, item, grid_offset_x, grid_offset_y, cell_size)

        # Draw Snake
        for p in players:
            for snake_case in p["snake"]:
                if (
                    p["head"][0] >= 0 
                    and p["head"][0] < grid_size 
                    and p["head"][1] >= 0 
                    and p["head"][1] < grid_size
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
        for p in players:
            for snake_case in p["snake"]:
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
        for p in players:
            game.draw_score(screen, p, width, height)
        
        # Print PAUSED
        menu.print_game_result(screen, "PAUSED", width, height)
        
    elif game_state == "GAME_OVER":
        
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Save Highscore
        save.save_highscores(highscores)
        
        # Print GAME OVER
        menu.print_game_result(screen, "GAME OVER", width, height)
        
        # Draw Score
        for p in players:
            game.draw_score(screen, p, width, height)
        
        # Buttons
        buttons = menu.draw_game_over(screen, width, height)
        
        # Grid Size and Cell Size Check
        grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
        
    elif game_state == "WIN":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        # Save Highscore
        save.save_highscores(highscores)
        
        # Print YOU WIN
        menu.print_game_result(screen, "YOU WIN", width, height)
        
        # Draw Score
        for p in players:
            game.draw_score(screen, p, width, height)
        
        # Buttons
        buttons = menu.draw_game_over(screen, width, height)
        
        # Grid Size and Cell Size Check
        grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
        
    elif game_state == "PLAYER_WIN":
        # Set screen color
        screen.fill(settings.BACKGROUND_COLOR)
        
        if winner == "P1":
            text = "PLAYER 1 WIN"
        elif winner == "P2":
            text = "PLAYER 2 WIN"
        else:
            text = "EQUALITY"
        
        # Save Highscore
        save.save_highscores(highscores)
        
        # Print YOU WIN
        menu.print_game_result(screen, text, width, height)
        
        # Draw Score
        for p in players:
            game.draw_score(screen, p, width, height)
        
        # Buttons
        buttons = menu.draw_game_over(screen, width, height)
        
        # Grid Size and Cell Size Check
        grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
        
    # Print
    pygame.display.flip()
    
    # Clock
    dt = clock.tick(settings.FPS) / 1000

pygame.quit()
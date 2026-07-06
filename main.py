import pygame
from collections import deque

import settings
import assets
import food
import snake
import game
import grid
import menu
import save
import audio
import bot

# Pygame Setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(
    (settings.DEFAULT_WIDTH, settings.DEFAULT_HEIGHT),
    pygame.RESIZABLE
)
assets.load_assets()
clock = pygame.time.Clock()
running = True
dt = 0

# Setup
game_state = "MENU"
menu_state = "PRINCIPAL"
mode = "SOLO"
obstacle_mode = False
powerup_mode = False
bot_mode = False
board_mode = "1-BOARD"
best_score = 0
difficulty = settings.NORMAL
difficulty_name = difficulty["name"]
max_obstacles = difficulty["max_obstacles"]
max_powerup = difficulty["max_power_up"]
powerup_interval = difficulty["power_up_interval"]
highscores = save.load_highscores()
players = []
text = None
marge = settings.DEFAULT_TITLE_MARGE

width = screen.get_width()
height = screen.get_height()

# Menu
buttons = deque([])
buttons = menu.draw_menu(screen, width, height, settings.MENUS[menu_state], marge)

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
                        mode = value
                        menu_state = "DIFFICULTY"
                        
                    elif value == "VERSUS":
                        mode = value
                        menu_state = "SELECT_PLAYER"
                        
                    elif value == "P1 VS P2":
                        bot_mode = False
                        menu_state = "SELECT_BOARD"
                        
                    elif value == "P1 VS IA":
                        bot_mode = True
                        menu_state = "SELECT_BOARD"
                        
                    elif value == "1-BOARD":
                        board_mode = value
                        menu_state = "DIFFICULTY"
                        
                    elif value == "2-BOARD":
                        board_mode = value
                        menu_state = "DIFFICULTY"
                        
                    elif value == "EASY":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.EASY)
                        if obstacle_mode:
                            max_obstacles = game.obstacle_game_setup(settings.EASY)
                        if powerup_mode:
                            max_powerup, powerup_interval = game.powerup_game_setup(settings.EASY)
                        
                    elif value == "NORMAL":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.NORMAL)
                        if obstacle_mode:
                            max_obstacles = game.obstacle_game_setup(settings.NORMAL)
                        if powerup_mode:
                            max_powerup, powerup_interval = game.powerup_game_setup(settings.NORMAL)
                        
                    elif value == "HARD":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.HARD)
                        if obstacle_mode:
                            max_obstacles = game.obstacle_game_setup(settings.HARD)
                        if powerup_mode:
                            max_powerup, powerup_interval = game.powerup_game_setup(settings.HARD)
                        
                    elif value == "INSANE":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(settings.ULTRA_HARD)
                        if obstacle_mode:
                            max_obstacles = game.obstacle_game_setup(settings.ULTRA_HARD)
                        if powerup_mode:
                            max_powerup, powerup_interval = game.powerup_game_setup(settings.ULTRA_HARD)
                        
                    elif value == "TRY AGAIN":
                        selected_grid_size, max_food, food_interval, game_state, difficulty = game.game_setup(difficulty)
                        if obstacle_mode:
                            max_obstacles = game.obstacle_game_setup(difficulty)
                        if powerup_mode:
                            max_powerup, powerup_interval = game.powerup_game_setup(difficulty)
                        
                    elif value == "MENU":
                        game_state = "MENU"
                        menu_state = "PRINCIPAL"
                        best_score = 0
                        
                    elif value == "RETURN":
                        if mode == "SOLO":
                            menu_state = "PRINCIPAL"
                        else:
                            if menu_state == "SELECT_PLAYER":
                                menu_state = "PRINCIPAL"
                            elif menu_state == "SELECT_BOARD":
                                menu_state = "SELECT_PLAYER"
                            elif menu_state == "DIFFICULTY":
                                menu_state = "SELECT_BOARD"
                        
                    elif value == "OBSTACLE":
                        obstacle_mode = False if obstacle_mode else True
                        
                    elif value == "POWERUP":
                        powerup_mode = False if powerup_mode else True
                    
                    # New Game
                    grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
                    difficulty_name = difficulty["name"]                
                    players, food_pos, free_cases, food_interval, obstacles_pos, powerup_pos, text = game.new_game(
                        selected_grid_size, 
                        max_food, 
                        food_interval,
                        difficulty,
                        mode,
                        bot_mode
                    )
                    if obstacle_mode:
                        obstacles_pos, powerup_pos = game.new_obstacle_game(
                            grid_size, 
                            food_pos, 
                            max_obstacles, 
                            players
                        )
                    if powerup_mode:
                        powerup_pos, powerup_interval = game.new_powerup_game(
                            grid_size, 
                            food_pos,  
                            max_powerup, 
                            difficulty,
                            players,
                            obstacles_pos
                        )

    # Menus
    if game_state == "MENU":
        
        # Set screen color
        # screen.fill(settings.BACKGROUND_COLOR)
        screen.blit(
            assets.get_sprite(
                assets.BACKGROUND,
                width,
                height
            ),
            (0, 0)
        )
        
        # Draw Difficulty Menu
        marge = (
            settings.DEFAULT_TITLE_MARGE 
            if menu_state != "DIFFICULTY" 
            else settings.DEFAULT_DIFFICULTY_MARGE
        )
        buttons = menu.draw_menu(screen, width, height, settings.MENUS[menu_state], marge)
        if menu_state != "PRINCIPAL":
            buttons = menu.draw_second_menu(
                screen, 
                buttons, 
                obstacle_mode, 
                powerup_mode, 
                width, 
                height, 
                settings.MENUS[menu_state],
                marge
            )
        
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
            
            game.update_effects(p, dt)

        # Move
        for p in players:
            if p["snake_len"] > 0:
                if p["name"] == "bot":
                    
                    p["next_direction"] = bot.update_bot_direction(
                        p, 
                        food_pos, 
                        obstacles_pos, 
                        powerup_pos, 
                        players, 
                        grid_size
                    )
                game.move(p)

        # Eat food
        for p in players:
            food_pos, max_food, food_interval, game_state, text = food.eat_food_check(
                p,
                players,
                grid_size,
                difficulty,
                game_state,
                obstacles_pos,
                food_pos,
                powerup_pos,
                max_food,
                food_interval,
                mode
            )
            
        # Eat Power Up
        if powerup_mode:
            for p in players:
                game_state, text, powerup_pos, max_powerup, powerup_interval = food.eat_powerup_check(
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
                    mode,
                    text
                )
        
        # Best Score Check
        mode2 = "EXTRA" if obstacle_mode or powerup_mode else "CLASSIC"
        for p in players:
            p["best_score"] = game.best_score_check(p, highscores, mode2, difficulty_name)
        
        # Speed & Len Check
        for p in players:
            p["speed"] = round(1 / p["move_interval"], 1)
            p["snake_len"] = len(p["snake"])
    
        # Grid-Out & Que-Eating & Multiplayer Collisions Check
        if mode != "SOLO":
            text, game_state = game.hit_player_check(
                players[0]["head"], 
                players[1]["head"], 
                players[0]["snake"], 
                players[1]["snake"],
                game_state,
                text
            )
        for p in players:
            if game.grid_out_check(p["head"], grid_size) or game.eat_que_check(p["snake"], p["head"]) or p["snake_len"] <= 0:
                if mode == "SOLO":
                    game_state, text = "GAME_OVER", "GAME OVER"
                    audio.LOSE_SOUND.play()
                else:
                    if p["name"] == "player_1":
                        game_state, text = "GAME_OVER", "P2 WIN"
                    else:
                        game_state, text = "GAME_OVER", "P1 WIN"
                    audio.WIN_SOUND.play()
        
        # Hit-Obstacles Check
        if obstacle_mode:
            for p in players:
                if game.hit_obstacles_check(p["head"], obstacles_pos):
                    if mode == "SOLO":
                        game_state, text = "GAME_OVER", "GAME OVER"
                        audio.LOSE_SOUND.play()
                    else:
                        if p["name"] == "player_1":
                            game_state, text = "GAME_OVER", "P2 WIN"
                        else:
                            game_state, text = "GAME_OVER", "P1 WIN"
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
            if (
                p["head"][0] >= 0 
                and p["head"][0] < grid_size 
                and p["head"][1] >= 0 
                and p["head"][1] < grid_size
            ):
                snake.draw_snake(
                    screen, 
                    p,
                    grid_offset_x, 
                    grid_offset_y, 
                    cell_size
                )
                    
        # Draw Obstacles    
        if obstacle_mode:
            for item in obstacles_pos:
                
                grid.draw_obstacles(screen, item, grid_offset_x, grid_offset_y, cell_size)
                
        # Draw Power Up   
        if powerup_mode:
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
            snake.draw_snake(screen, p, grid_offset_x, grid_offset_y, cell_size)
        
        # Draw Obstacles
        if obstacle_mode:
            for item in obstacles_pos:
                grid.draw_obstacles(screen, item, grid_offset_x, grid_offset_y, cell_size)
                
        # Draw Power Up
        if powerup_mode: 
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
        
        buttons, grid_size, cell_size = game.end_game(
            screen, 
            highscores, 
            players, 
            width, 
            height, 
            selected_grid_size, 
            text,
            game_state
        )
        
    # Print
    pygame.display.flip()
    
    # Clock
    dt = clock.tick(settings.FPS) / 1000

pygame.quit()
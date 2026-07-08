import random
import pygame

import game
import snake
import food
import settings
import menu
import grid
import audio
import save
import assets

def cell_size_check(selected_grid_size, width, height):
    
    grid_size = selected_grid_size
    cell_size = min(width, height - 150) // grid_size
    
    return grid_size, cell_size

def offsetts_check(width, height, grid_size, cell_size):
    
    grid_offset_x = (width - grid_size * cell_size) / 2
    grid_offset_y = 75 + (((height - 150) - grid_size * cell_size) / 2)
    
    return grid_offset_x, grid_offset_y

def free_case_check(grid_size, max_food, players):
    
    grid_len = grid_size ** 2
    
    snake_len = 0
    for p in players:
        for _ in p["snake"]:
            snake_len += 1
        
    return grid_len - snake_len - max_food

def speed_adjustment(player):
    
    while player["score"] >= player["speed_limit"]:
        player["base_move_interval"] *= 0.98
        player["speed_limit"] += 5
        
def has_effect(player, effect_type):

    return any(
        effect["type"] == effect_type
        for effect in player["effects"]
    )

def create_player(grid_size, difficulty, controls, name):
    
    new_snake = snake.generate_snake(grid_size)
    direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
    
    player = {
        "name": name,
        
        "snake": new_snake,
        "head": new_snake[0],
        
        "direction": direction,
        "next_direction": direction,
        
        "score": 0,
        "best_score": 0,
        "speed_limit": 5,
        
        "grow": False,
        
        "move_timer": 0,
        "base_move_interval": difficulty["move_interval"],
        "move_interval": difficulty["move_interval"],
        
        "effects": [],
        
        "speed": round(1 / difficulty["move_interval"], 1),
        "snake_len": len(new_snake),
        
        "controls": controls
    }
    
    return player

def new_game(grid_size, max_food, food_interval, difficulty, mode, bot_mode):
    
    if mode == "SOLO":
        player = create_player(
            grid_size,
            difficulty,
            settings.SOLO_CONTROLS,
            "player_1"
        )
        players = [player]
    else:
        player1 = create_player(
            grid_size,
            difficulty,
            settings.SOLO_CONTROLS if bot_mode else settings.MULTI_P1_CONTROLS,
            "player_1"
        )
        player2 = create_player(
            grid_size,
            difficulty,
            {} if bot_mode else settings.MULTI_P2_CONTROLS,
            "bot" if bot_mode else "player_2"
        )
        players = [player1, player2]
    
    # Obstacles
    obstacles_pos = []
    
    # Power Up & Down
    powerup_pos = []
    
    # Food
    food_pos = []
    for _ in range(max_food):
        food_pos.append(food.generate_food(grid_size, food_pos, powerup_pos, obstacles_pos, players))
        
    food_interval = (max_food - 1) * difficulty["food_interval"]
    
    # Free Cases
    free_cases = free_case_check(grid_size, max_food, players)
    
    # Winner
    text = None
    
    return players, food_pos, free_cases, food_interval, obstacles_pos, powerup_pos, text

def new_obstacle_game(grid_size, food_pos, max_obstacles, players):
    
    powerup_pos = []
    obstacles_pos = []
    occupied_cases = []
    
    max_obstacle_len = grid_size // 4
    possible_direction = ["UP", "LEFT", "DOWN", "RIGHT"]
    
    for p in players:
        occupied_cases.extend(p["snake"])

    occupied_cases.extend(food_pos)
    occupied_cases.extend(obstacles_pos)
    occupied_cases.extend(powerup_pos)
    
    for _ in range(max_obstacles):
        
        obstacle_len = random.randint(1, max_obstacle_len)
        obstacle = grid.generate_obstacles(grid_size, food_pos, obstacles_pos, players)
        obstacles_pos.append(obstacle)
        occupied_cases.append(obstacle)
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
                or next_obstacle in occupied_cases
            ):
                break
            
            obstacle = next_obstacle
            obstacles_pos.append(obstacle)
            occupied_cases.append(obstacle)
    
    return obstacles_pos, powerup_pos

def new_powerup_game(grid_size, food_pos, max_powerup, difficulty, players, obstacles_pos):
    
    powerup_pos = []
    
    for _ in range(max_powerup):
        powerup_pos.append(food.generate_powerup(
            grid_size,
            food_pos, 
            powerup_pos, 
            obstacles_pos, 
            players
        ))
                
    powerup_interval = (max_powerup - 1) * difficulty["power_up_interval"] if max_powerup > 1 else 1
    
    return powerup_pos, powerup_interval

def turn(next_direction, ingame_snake, grow):
    
    direction = next_direction
    
    ingame_snake, grow = snake.add_snake_case(
        direction, 
        ingame_snake, 
        grow
    
    )
    head = ingame_snake[0]
            
    return direction, ingame_snake, grow, head

def update_player(player):
    
    player["direction"], player["snake"], player["grow"], player["head"] = turn(
        player["next_direction"],
        player["snake"],
        player["grow"]
    )
    
def move(player):
    
    if player["move_timer"] >= player["move_interval"]:

        player["move_timer"] = 0

        for effect in player["effects"][:]:
            if (
                effect["type"] == "GROW" 
                or effect["type"] == "POISON" 
                or effect["type"] == "SCORE_UP" 
                or effect["type"] == "SCORE_DOWN"
            ):
                if effect["remaining"] == 1:
                    player["score"] = (
                        player["score"] + settings.EFFECTS[effect["type"]]["boost"] 
                        if player["score"] > -(settings.EFFECTS[effect["type"]]["boost"])
                        else 0
                    )
                    
                if effect["type"] != "POISON":
                    player["grow"] = True

                effect["remaining"] -= 1

                if effect["remaining"] <= 0:
                    player["effects"].remove(effect)

        update_player(player)

def update_effects(player, dt):
    
    player["move_interval"] = player["base_move_interval"]
    
    for effect in player["effects"][:]:
        if effect["type"] == "SPEED" or effect["type"] == "FREEZE":

            effect["remaining"] -= dt

            if effect["remaining"] <= 0:
                player["effects"].remove(effect)
                continue

            player["move_interval"] *= settings.EFFECTS[effect["type"]]["boost"]

def reset_powerup(players, head, food_pos, powerup_pos, powerup_interval, obstacles_pos, grid_size, difficulty, free_cases, max_powerup):
    
    # Generate Powerup
    for i, item in enumerate(powerup_pos):
        if item["pos"] == head:
            powerup_pos[i] = food.generate_powerup(
                grid_size,
                food_pos,
                powerup_pos,
                obstacles_pos,
                players
            )
                        
    # Powerup Downgrade
    if free_cases <= powerup_interval:
        max_powerup -= 1
        powerup_interval = (max_powerup - 1) * difficulty["power_up_interval"] if max_powerup > 1 else 1
        powerup_pos.pop()
        
    return powerup_pos, max_powerup, powerup_interval

def best_score_check(player, highscores, mode2, difficulty_name):
    
    if player["score"] > highscores[mode2][difficulty_name]:
            highscores[mode2][difficulty_name] = player["score"]
        
    best_score = highscores[mode2][difficulty_name]
    
    return best_score

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

def hit_player_check(head1, head2, snake1, snake2, game_state, text):
    
    if head1 == head2:
        audio.LOSE_SOUND.play()
        game_state = "GAME_OVER"
        return "EGALITY", game_state
    
    if head1 in snake2:
        audio.WIN_SOUND.play()
        game_state = "GAME_OVER"
        return "P2 WIN", game_state
    
    if head2 in snake1:
        audio.WIN_SOUND.play()
        game_state = "GAME_OVER"
        return "P1 WIN", game_state
    
    return text, game_state

def game_setup(difficulty):
    
    selected_grid_size = difficulty["grid_size"]
    max_food = difficulty["max_food"]
    food_interval = difficulty["food_interval"]
    game_state = "GAME"
    
    return selected_grid_size, max_food, food_interval, game_state, difficulty

def obstacle_game_setup(difficulty):
    
    max_obstacles = difficulty["max_obstacles"]
    
    return max_obstacles

def powerup_game_setup(difficulty):
    
    max_powerup = difficulty["max_power_up"]
    powerup_interval = difficulty["power_up_interval"]
    
    return max_powerup, powerup_interval

def create_rect(x, y, width, height):
    return pygame.Rect(
        x, 
        y,
        width, 
        height
    )

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

def draw_score(screen, player, width, height):
    
    dw, dh = menu.get_scale(width, height)
    
    score_width = max(settings.DEFAULT_SCORE_MIN_WIDTH, int(settings.DEFAULT_SCORE_WIDTH * dw))
    score_height = max(settings.DEFAULT_SCORE_MIN_HEIGHT, int(settings.DEFAULT_SCORE_HEIGHT * dh))
    
    x = int(20 * dh) if player["name"] == "player_1" else width - int(20 * dh) - score_width
    
    score_font = assets.create_font(settings.DEFAULT_SCORE_FONT, dh)
    
    sprite = assets.SCREEN
    
    score_rect = create_rect(x, int((30 * dh) + score_height), score_width, score_height)
    best_score_rect = create_rect(x, int(20 * dh), score_width, score_height)
    speed_rect = create_rect(x, int((40 * dh) + score_height * 2), score_width, score_height)
    snake_len_rect = create_rect(x, int((50 * dh) + score_height * 3), score_width, score_height)
    
    menu.draw_button(screen, score_rect, f"SCORE:\n{player['score']}", sprite, score_font, settings.SCORE_COLOR)
    menu.draw_button(screen, best_score_rect, f"BEST:\n{player['best_score']}", sprite, score_font, settings.SCORE_COLOR)
    menu.draw_button(screen, speed_rect, f"SPEED:\n{player['speed']} C/s", sprite, score_font, settings.SCORE_COLOR)
    menu.draw_button(screen, snake_len_rect, f"LENGHT:\n{player['snake_len']}", sprite, score_font, settings.SCORE_COLOR)
    
def end_game(screen, highscores, players, width, height, selected_grid_size, text, game_state):
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
        
    # Save Highscore
    save.save_highscores(highscores)
        
    # Draw Score
    for p in players:
        game.draw_score(screen, p, width, height)
        
    # Buttons
    buttons = menu.draw_game_over(screen, width, height, settings.MENUS[game_state])
    
    # Print GAME OVER
    menu.print_game_result(screen, text, width, height)
        
    # Grid Size and Cell Size Check
    grid_size, cell_size = game.cell_size_check(selected_grid_size, width, height)
    
    return buttons, grid_size, cell_size
    
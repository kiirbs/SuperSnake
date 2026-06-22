import pygame
import random

import game
import audio
import settings

def generate_food(grid_size, food_pos, obstacles_pos, players):
    
    possible_food_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if not any(
            [i, j] in p["snake"]
            for p in players
        )
        and [i, j] not in food_pos
        and [i, j] not in obstacles_pos
    ]
    
    if not possible_food_pos:
        return None
    
    return random.choice(possible_food_pos)

def draw_food(screen, food_pos, grid_offset_x, grid_offset_y, cell_size):
    
    food_row = food_pos[0]
    food_col = food_pos[1]
    
    pygame.draw.rect(
            screen,
            settings.FOOD_COLOR,
            (
                grid_offset_x + food_row * cell_size + 1,
                grid_offset_y + food_col * cell_size + 1,
                cell_size - 2,
                cell_size - 2
            )
        )
    
def generate_powerup(grid_size, food_pos, powerup_pos, obstacles_pos, players):
    
    possible_effect = ["POISON", "SPEED", "SCORE", "BONUS"]
    
    possible_powerup_pos = [
        [i, j]
        for i in range(grid_size) 
        for j in range(grid_size)
        if not any(
            [i, j] in p["snake"]
            for p in players
        )
        and [i, j] not in food_pos 
        and [i, j] not in obstacles_pos 
        and [i, j] not in powerup_pos
    ]
    
    if not possible_powerup_pos:
        return None
    
    powerup = {
        "pos": random.choice(possible_powerup_pos),
        "type": random.choice(possible_effect)
    }
    
    return powerup

def draw_powerup(screen, pos, type, grid_offset_x, grid_offset_y, cell_size):

    row = pos[0]
    col = pos[1]
    
    if type == "POISON":
        color = settings.POISON_COLOR
    if type == "SPEED":
        color = settings.SPEED_COLOR
    if type == "SCORE":
        color = settings.SCORE_UP_COLOR
    if type == "BONUS":
        color = settings.BONUS_COLOR
    
    pygame.draw.rect(
            screen,
            color,
            (
                grid_offset_x + row * cell_size + 1,
                grid_offset_y + col * cell_size + 1,
                cell_size - 2,
                cell_size - 2
            )
        )
    
def eat_food_check(player, players, grid_size, difficulty, game_state, obstacles_pos, food_pos, max_food, food_interval, mode):
    
    text = None
    
    if player["head"] in food_pos:
        player["score"] += 1
        player["grow"] = True
        free_cases = game.free_case_check(grid_size, max_food, players)
        player["move_interval"], player["old_move_interval"], player["speed_limit"] = game.speed_adjustment(
            player["score"], 
            player["speed_limit"], 
            player["move_interval"], 
            player["old_move_interval"]
        )
        audio.FOOD_SOUND.play()
                
        # Generate Food
        for i, item in enumerate(food_pos):
            if item == player["head"]:
                food_pos[i] = generate_food(
                    grid_size, 
                    food_pos,
                    obstacles_pos,
                    players
                )
                        
        # Food Downgrade
        if free_cases <= food_interval:
            max_food -= 1
            food_interval = (max_food - 1) * difficulty["food_interval"]
            food_pos.pop()
                    
            if free_cases <= 0:
                if mode == "SOLO":
                    game_state, text = "GAME_OVER", "YOU WIN"
                else:
                    game_state, text = "GAME_OVER", "EGALITY"
                audio.WIN_SOUND.play()
                        
    return food_pos, max_food, food_interval, game_state, text

def eat_powerup_check(player, players, grid_size, difficulty, game_state, obstacles_pos, food_pos, max_food, powerup_pos, max_powerup, powerup_interval, mode, text):
        
    for powerup in powerup_pos:
                
        if powerup is None:
            continue
                    
        if player["head"] == powerup["pos"]:
            free_cases = game.free_case_check(grid_size, max_food, players)
                    
            if powerup["type"] == "POISON":
                player["score"] -= 1
                player["snake"].pop()
                audio.POISON_SOUND.play()
                        
                if len(player["snake"]) <= 0 or player["score"] < 0:
                    if mode == "SOLO":
                        game_state, text = "GAME_OVER", "GAME OVER"
                        audio.LOSE_SOUND.play()
                    else:
                        if player["name"] == "player_1":
                            game_state, text = "GAME_OVER", "P2 WIN"
                        else:
                            game_state, text = "GAME_OVER", "P1 WIN"
                        audio.WIN_SOUND.play()
                            
                powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                    players,
                    player["head"], 
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
                player["score"] += 1
                player["grow"] = True
                audio.POWERUP_SOUND.play()
                        
                if player["speed_end_timer"] <= 0:
                    player["old_move_interval"] = player["move_interval"]
                    player["move_interval"] *= 0.75
                    player["speed_end_timer"] = 5
                else:
                    player["speed_end_timer"] = 5
                        
                player["move_interval"], player["old_move_interval"], player["speed_limit"] = game.speed_adjustment(
                    player["score"], 
                    player["speed_limit"], 
                    player["move_interval"], 
                    player["old_move_interval"]
                )
                powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                    players,
                    player["head"], 
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
                player["score"] += 5
                player["grow"] = True
                audio.POWERUP_SOUND.play()
                        
                player["move_interval"], player["old_move_interval"], player["speed_limit"] = game.speed_adjustment(
                    player["score"], 
                    player["speed_limit"], 
                    player["move_interval"], 
                    player["old_move_interval"]
                )
                powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                    players,
                    player["head"],
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
                player["score"] += 1
                player["grow"] = True
                player["bonus_grow"] = True
                player["bonus_timer"] = 5
                audio.POWERUP_SOUND.play()
                        
                player["move_interval"], player["old_move_interval"], player["speed_limit"] = game.speed_adjustment(
                    player["score"], 
                    player["speed_limit"], 
                    player["move_interval"], 
                    player["old_move_interval"]
                )
                powerup_pos, max_powerup, powerup_interval = game.reset_powerup(
                    players,
                    player["head"],
                    food_pos, 
                    powerup_pos, 
                    powerup_interval,
                    obstacles_pos, 
                    grid_size, 
                    difficulty, 
                    free_cases, 
                    max_powerup
                )
                
    return game_state, text, powerup_pos, max_powerup, powerup_interval
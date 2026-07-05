import random

import game
import audio
import assets
import settings

def generate_food(grid_size, food_pos, powerup_pos, obstacles_pos, players):
    
    possible_food_pos = [
        [i, j]
        for i in range(grid_size)
        for j in range(grid_size)
        if (
            not any([i, j] in p["snake"] for p in players)
            and [i, j] not in food_pos
            and [i, j] not in obstacles_pos
            and not any(
                powerup is not None and powerup["pos"] == [i, j]
                for powerup in powerup_pos
            )
        )
    ]
    
    if not possible_food_pos:
        return None
    
    return random.choice(possible_food_pos)

def draw_food(screen, food_pos, grid_offset_x, grid_offset_y, cell_size):
    
    food_row = food_pos[0]
    food_col = food_pos[1]
    
    sprite = assets.get_sprite(
        assets.FOOD,
        cell_size
    )
    
    screen.blit(
        sprite,
        (
            grid_offset_x + food_row * cell_size,
            grid_offset_y + food_col * cell_size
        )
    )
    
def generate_powerup(grid_size, food_pos, powerup_pos, obstacles_pos, players):
        
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
        "type": random.choice(settings.POSSIBLE_EFFECTS)
    }
    
    return powerup

def draw_powerup(screen, pos, type, grid_offset_x, grid_offset_y, cell_size):

    row = pos[0]
    col = pos[1]
    
    sprite = assets.get_sprite(
        assets.POWERUPS[type],
        cell_size
    )
    
    screen.blit(
        sprite,
        (
            grid_offset_x + row * cell_size,
            grid_offset_y + col * cell_size
        )
    )
    
def eat_food_check(
    player, 
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
):
    
    text = None
    
    if player["head"] in food_pos:
        player["score"] += 1
        player["grow"] = True
        free_cases = game.free_case_check(grid_size, max_food, players)
        game.speed_adjustment(player)
        audio.FOOD_SOUND.play()
                
        # Generate Food
        for i, item in enumerate(food_pos):
            if item == player["head"]:
                food_pos[i] = generate_food(
                    grid_size, 
                    food_pos,
                    powerup_pos,
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

def apply_poison(player):
    
    player["effects"].append({
        "type": "POISON",
        "remaining": settings.EFFECTS["POISON"]["duration"]
    })
    player["snake"].pop()
    audio.POISON_SOUND.play()
    
def apply_speed(player):
    
    player["score"] += 1
    player["grow"] = True
    audio.POWERUP_SOUND.play()
        
    for effect in player["effects"]:
        if effect["type"] == "SPEED":
            effect["remaining"] = settings.EFFECTS["SPEED"]["duration"]
            return
        
    player["effects"].append({
        "type": "SPEED",
        "remaining": settings.EFFECTS["SPEED"]["duration"]
    })
    
def apply_freeze(player):
    
    player["score"] += 1
    player["grow"] = True
    audio.POWERUP_SOUND.play()
                        
    for effect in player["effects"]:
        if effect["type"] == "FREEZE":
            effect["remaining"] = settings.EFFECTS["FREEZE"]["duration"]
            return
        
    player["effects"].append({
        "type": "FREEZE",
        "remaining": settings.EFFECTS["FREEZE"]["duration"]
    })
    
def apply_score_up(player):
    
    player["effects"].append({
        "type": "SCORE_UP",
        "remaining": settings.EFFECTS["SCORE_UP"]["duration"]
    })
    audio.POWERUP_SOUND.play()
    
def apply_score_down(player):
    
    player["effects"].append({
        "type": "SCORE_DOWN",
        "remaining": settings.EFFECTS["SCORE_DOWN"]["duration"]
    })
    audio.POWERUP_SOUND.play()
    
def apply_grow(player):
    
    player["effects"].append({
        "type": "GROW",
        "remaining": settings.EFFECTS["GROW"]["duration"]
    })
    
APPLY_EFFECT = {
    "SPEED": apply_speed,
    "FREEZE": apply_freeze,
    "POISON": apply_poison,
    "GROW": apply_grow,
    "SCORE_UP": apply_score_up,
    "SCORE_DOWN": apply_score_down,
}

def eat_powerup_check(
    player, 
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
):
    
    for powerup in powerup_pos:
                
        if powerup is None:
            continue
                    
        if player["head"] == powerup["pos"]:
            
            effect = powerup["type"]
            free_cases = game.free_case_check(grid_size, max_food, players)
                    
            effect_func = APPLY_EFFECT.get(effect)

            if effect_func:
                effect_func(player)
            
            if effect != "POISON" and effect != "SCORE_DOWN":
                game.speed_adjustment(player)
            
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
                
    return game_state, text, powerup_pos, max_powerup, powerup_interval
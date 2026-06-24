import random
from collections import deque

def get_opp_head(players, blocked):
    
    enemy = next(
        p for p in players
        if p["name"] != "bot"
    )
    
    enemy_head = enemy["head"]

    if enemy["direction"] == "UP":
        blocked.add((enemy_head[0], enemy_head[1] - 1))

    elif enemy["direction"] == "DOWN":
        blocked.add((enemy_head[0], enemy_head[1] + 1))

    elif enemy["direction"] == "LEFT":
        blocked.add((enemy_head[0] - 1, enemy_head[1]))

    elif enemy["direction"] == "RIGHT":
        blocked.add((enemy_head[0] + 1, enemy_head[1]))
        
    return blocked

def get_blocked_cases(players, obstacles_pos):

    blocked = set()
    
    if len(players) < 2:
        return blocked
    
    blocked = get_opp_head(players, blocked)

    for player in players:
        
        snake_body = list(player["snake"])
        
        if player["name"] == "bot":
            if not player["grow"]:
                for case in snake_body[1:-1]:
                    blocked.add(tuple(case))
            else:
                for case in snake_body[1:]:
                    blocked.add(tuple(case))
        else:
            if not player["grow"]:
                for case in snake_body[:-1]:
                    blocked.add(tuple(case))
            else:
                for case in snake_body:
                    blocked.add(tuple(case))

    for obstacle in obstacles_pos:
        blocked.add(tuple(obstacle))

    return blocked

def find_path_bfs(start, target, players, obstacles_pos, grid_size):
    
    blocked = get_blocked_cases(players, obstacles_pos)

    queue = deque([start])

    visited = {start}

    parent = {}

    directions = [
        (0, -1),  # UP
        (0, 1),   # DOWN
        (-1, 0),  # LEFT
        (1, 0)    # RIGHT
    ]

    while queue:

        x, y = queue.popleft()

        if (x, y) == target:

            path = []

            current = target

            while current != start:
                path.append(current)
                current = parent[current]

            path.reverse()

            return path

        for dx, dy in directions:

            nx = x + dx
            ny = y + dy

            next_case = (nx, ny)

            if (
                nx < 0
                or nx >= grid_size
                or ny < 0
                or ny >= grid_size
            ):
                continue

            if next_case in blocked:
                continue

            if next_case in visited:
                continue

            visited.add(next_case)

            parent[next_case] = (x, y)

            queue.append(next_case)

    return None

def check_best_path(head, food_pos, powerup_pos, players, obstacles_pos, grid_size):
    
    best_item = None
    best_path = None

    for food in food_pos:

        path = find_path_bfs(
            tuple(head),
            tuple(food),
            players,
            obstacles_pos,
            grid_size
        )

        if path is None:
            continue

        if best_path is None or len(path) < len(best_path):
            best_path = path
            best_item = food    
    
    for powerup in powerup_pos:
        
        if powerup is None:
            continue

        if powerup["type"] == "POISON":
            continue
            
        path = find_path_bfs(
            tuple(head),
            tuple(powerup["pos"]),
            players,
            obstacles_pos,
            grid_size
        )

        if path is None:
            continue

        if best_path is None or len(path) < len(best_path):
            best_path = path
            best_item = powerup["pos"]
            
    return best_path, best_item

def get_next_direction(head, path):
    
    if not path:
        return None

    next_x, next_y = path[0]

    dx = next_x - head[0]
    dy = next_y - head[1]

    if dx == 1:
        return "RIGHT"

    if dx == -1:
        return "LEFT"

    if dy == 1:
        return "DOWN"

    if dy == -1:
        return "UP"

def get_possible_direction(head_x, head_y, direction, obstacles_pos, players, grid_size):
    
    directions = ["UP", "LEFT", "DOWN", "RIGHT"]
    
    blocked = get_blocked_cases(players, obstacles_pos)
        
    if direction == "UP":
        directions.remove("DOWN")
    elif direction == "LEFT":
        directions.remove("RIGHT")
    elif direction == "DOWN":
        directions.remove("UP")
    elif direction == "RIGHT":
        directions.remove("LEFT")
    
    actual_case = (head_x - 1, head_y)
    if (
        actual_case in blocked
        or actual_case[0] < 0
    ):
        if "LEFT" in directions:
            directions.remove("LEFT")
    
    actual_case = (head_x + 1, head_y)
    if (
        actual_case in blocked
        or actual_case[0] >= grid_size
    ):
        if "RIGHT" in directions:
            directions.remove("RIGHT")
    
    actual_case = (head_x, head_y - 1)
    if (
        actual_case in blocked
        or actual_case[1] < 0
    ):
        if "UP" in directions:
            directions.remove("UP")
    
    actual_case = (head_x, head_y + 1)
    if (
        actual_case in blocked
        or actual_case[1] >= grid_size
    ):
        if "DOWN" in directions:
            directions.remove("DOWN")
            
    return directions

def update_bot_direction(bot, food_pos, obstacles_pos, powerup_pos, players, grid_size):
        
    next_direction = None
    direction = bot["direction"]
    
    head_x = bot["head"][0]
    head_y = bot["head"][1]
    
    best_path, best_item = check_best_path(
        bot["head"], 
        food_pos, 
        powerup_pos, 
        players, 
        obstacles_pos, 
        grid_size
    )
    
    next_direction = get_next_direction(bot["head"], best_path)
    
    if next_direction is None:
        
        possible_directions = get_possible_direction(
            head_x, 
            head_y, 
            direction, 
            obstacles_pos, 
            players, 
            grid_size,
        )
        
        if len(possible_directions) > 0:
            next_direction = random.choice(possible_directions)
        else:
            next_direction = direction
    
    return next_direction
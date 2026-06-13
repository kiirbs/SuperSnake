DEFAULT_GRID_SIZE = 20

# Title Space
DEFAULT_TITLE_MARGE = 200

# 1st and 2nd Menu Buttons
DEFAULT_BUTTON_WIDTH = 550
DEFAULT_BUTTON_HEIGHT = 80
DEFAULT_BUTTON_MARGE = 20
DEFAULT_BUTTON_MIN_WIDTH = 100
DEFAULT_BUTTON_MIN_HEIGHT = 25
DEFAULT_BUTTON_MIN_MARGE = 5

# Return and Extra Button
DEFAULT_BUTTON2_WIDTH = 200
DEFAULT_BUTTON2_HEIGHT = 40
DEFAULT_BUTTON2_MIN_WIDTH = 50
DEFAULT_BUTTON2_MIN_HEIGHT = 12

# Game Over Buttons
DEFAULT_BUTTON3_WIDTH = 350
DEFAULT_BUTTON3_HEIGHT = 65
DEFAULT_BUTTON3_MARGE = 80
DEFAULT_BUTTON3_MIN_WIDTH = 50
DEFAULT_BUTTON3_MIN_HEIGHT = 12
DEFAULT_BUTTON3_MIN_MARGE = 5

# Score
DEFAULT_SCORE_WIDTH = 160
DEFAULT_SCORE_HEIGHT = 40
DEFAULT_SCORE_MIN_WIDTH = 25
DEFAULT_SCORE_MIN_HEIGHT = 6

# Pixels
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

# Fonts
DEFAULT_MENU_FONT = 64
DEFAULT_GAME_OVER_FONT = 32
DEFAULT_TITLE_FONT = 192
DEFAULT_SCORE_FONT = 32
DEFAULT_RETURN_FONT = 32
DEFAULT_EXTRA_FONT = 32

# Menu States
MENU = [
    "SOLO",
    "ONE-BOARD MULTI",
    "TWO-BOARD MULTI"
]

DIFFICULT = [
    "EASY",
    "NORMAL",
    "HARD",
    "ULTRA HARD"
]

GAME_OVER = [
    "TRY AGAIN",
    "RETURN TO MENU"
]

# Difficulties
EASY = {
    "grid_size": 10,
    "move_interval": 0.4,
    "max_food": 3,
    "food_interval": 33,
    "max_obstacles": 5,
    "max_power_up": 1,
    "power_up_interval": 0
}

NORMAL = {
    "grid_size": 20,
    "move_interval": 0.3,
    "max_food": 4,
    "food_interval": 100,
    "max_obstacles": 7,
    "max_power_up": 2,
    "power_up_interval": 100
}

HARD = {
    "grid_size": 30,
    "move_interval": 0.2,
    "max_food": 5,
    "food_interval": 180,
    "max_obstacles": 10,
    "max_power_up": 3,
    "power_up_interval": 300
}

ULTRA_HARD = {
    "grid_size": 40,
    "move_interval": 0.15,
    "max_food": 8,
    "food_interval": 200,
    "max_obstacles": 15,
    "max_power_up": 4,
    "power_up_interval": 400
}

# Colors
BACKGROUND_COLOR = (58, 58, 58)
GRID_COLOR = (5, 2, 3)
SNAKE_COLOR = (0, 128, 0)
FOOD_COLOR = (121, 6, 4)
MENU_COLOR = (0, 0, 0)
MENU_HOVER_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
TEXT_HOVER_COLOR = (255, 255, 0)
SCORE_COLOR = (0, 0, 0)
OBSTACLES_COLOR = (5, 2, 3)

# Fps
FPS = 60
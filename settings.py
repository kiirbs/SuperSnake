DEFAULT_GRID_SIZE = 20
DEFAULT_BUTTON_WIDTH = 400
DEFAULT_BUTTON_HEIGHT = 100
DEFAULT_BUTTON_MARGE = 20
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_MENU_FONT = 64
DEFAULT_GAME_OVER_FONT = 32

SCREEN_SIZES = [
    (1280, 720),
    (1600, 900),
    (1920, 1080)
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

EASY = {
    "grid_size": 10,
    "move_interval": 0.4,
    "max_food": 3,
    "food_interval": 33
}

NORMAL = {
    "grid_size": 20,
    "move_interval": 0.3,
    "max_food": 4,
    "food_interval": 100
}

HARD = {
    "grid_size": 30,
    "move_interval": 0.2,
    "max_food": 5,
    "food_interval": 180
}

ULTRA_HARD = {
    "grid_size": 40,
    "move_interval": 0.1,
    "max_food": 6,
    "food_interval": 200
}

BACKGROUND_COLOR = (58, 58, 58)
GRID_COLOR = (5, 2, 3)
SNAKE_COLOR = (0, 128, 0)
FOOD_COLOR = (121, 6, 4)
MENU_COLOR = (0, 0, 0)
MENU_HOVER_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
TEXT_HOVER_COLOR = (255, 255, 0)

FPS = 60
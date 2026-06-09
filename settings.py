DEFAULT_GRID_SIZE = 20

DEFAULT_TITLE_MARGE = 200

DEFAULT_BUTTON_WIDTH = 550
DEFAULT_BUTTON_HEIGHT = 80
DEFAULT_BUTTON_MARGE = 20
DEFAULT_BUTTON_MIN_WIDTH = 100
DEFAULT_BUTTON_MIN_HEIGHT = 25
DEFAULT_BUTTON_MIN_MARGE = 5

DEFAULT_BUTTON2_WIDTH = 200
DEFAULT_BUTTON2_HEIGHT = 40
DEFAULT_BUTTON2_MIN_WIDTH = 50
DEFAULT_BUTTON2_MIN_HEIGHT = 12

DEFAULT_BUTTON3_WIDTH = 350
DEFAULT_BUTTON3_HEIGHT = 65
DEFAULT_BUTTON3_MARGE = 80
DEFAULT_BUTTON3_MIN_WIDTH = 50
DEFAULT_BUTTON3_MIN_HEIGHT = 12
DEFAULT_BUTTON3_MIN_MARGE = 5

DEFAULT_SCORE_WIDTH = 160
DEFAULT_SCORE_HEIGHT = 40
DEFAULT_SCORE_MIN_WIDTH = 25
DEFAULT_SCORE_MIN_HEIGHT = 6

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

DEFAULT_MENU_FONT = 64
DEFAULT_GAME_OVER_FONT = 32
DEFAULT_TITLE_FONT = 192
DEFAULT_SCORE_FONT = 32
DEFAULT_RETURN_FONT = 32

SCREEN_SIZES = [
    (1280, 720),
    (1600, 900),
    (1920, 1080)
]

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

EASY = {
    "grid_size": 10,
    "move_interval": 0.4,
    "max_food": 3,
    "food_interval": 33,
    "max_obstacles": 25,
    "max_power_up": 1,
    "power_up_interval": 0
}

NORMAL = {
    "grid_size": 20,
    "move_interval": 0.3,
    "max_food": 4,
    "food_interval": 100,
    "max_obstacles": 100,
    "max_power_up": 2,
    "power_up_interval": 100
}

HARD = {
    "grid_size": 30,
    "move_interval": 0.2,
    "max_food": 5,
    "food_interval": 180,
    "max_obstacles": 225,
    "max_power_up": 3,
    "power_up_interval": 300
}

ULTRA_HARD = {
    "grid_size": 40,
    "move_interval": 0.1,
    "max_food": 8,
    "food_interval": 200,
    "max_obstacles": 400,
    "max_power_up": 4,
    "power_up_interval": 400
}

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

FPS = 60
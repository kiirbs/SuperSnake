import pygame

DEFAULT_GRID_SIZE = 20

# Marges
DEFAULT_TITLE_MARGE = 200
DEFAULT_DIFFICULTY_MARGE = 25

# 1st and 2nd Menu Buttons
DEFAULT_BUTTON_WIDTH = 400
DEFAULT_BUTTON_HEIGHT = 150
DEFAULT_BUTTON_MARGE = 20
DEFAULT_BUTTON_MIN_WIDTH = 100
DEFAULT_BUTTON_MIN_HEIGHT = 25
DEFAULT_BUTTON_MIN_MARGE = 5

# Return and Extra Button
DEFAULT_BUTTON2_WIDTH = 300
DEFAULT_BUTTON2_HEIGHT = 108
DEFAULT_BUTTON2_MIN_WIDTH = 50
DEFAULT_BUTTON2_MIN_HEIGHT = 12

# Settings Button
DEFAULT_SETTINGS_BUTTON_WIDTH = 125
DEFAULT_SETTINGS_BUTTON_HEIGHT = 125
DEFAULT_SETTINGS_BUTTON_MARGE = 175
SETTINGS_ICON_RATIO = 0.7
SETTINGS_HOVER_GROWTH = 10

# Settings Menu (dimensions dans la fenetre de reference 1280 x 720)
SETTINGS_MENU_MARGIN = 100
SETTINGS_MENU_TOP = 220
SETTINGS_COLUMN_WIDTH = 306
SETTINGS_ROW_HEIGHT = 112
SETTINGS_ROW_GAP = 36
SETTINGS_MENU_FONT = 24
SETTINGS_HEADING_FONT = 64
SETTINGS_TOGGLE_SIZE = 40
SETTINGS_SLIDER_HEIGHT = 70
SETTINGS_SLIDER_BOTTOM_MARGIN = 4
SETTINGS_VOLUME_FRAME_SIZE = 6
SETTINGS_VOLUME_PANEL_EXTRA_HEIGHT = 32
SETTINGS_VOLUME_FONT = 20
SETTINGS_VOLUME_REFERENCE_PIXEL_SCALE = 2
SETTINGS_DEFAULT_VOLUME = 0.5
SETTINGS_CONTROL_COLOR = (35, 53, 53)
SETTINGS_CONTROL_HOVER_COLOR = (56, 82, 82)
SETTINGS_BORDER_COLOR = (137, 163, 150)
SETTINGS_SELECTED_COLOR = (87, 113, 80)
SETTINGS_TEXT_COLOR = (235, 237, 216)

# Quit Game Button
DEFAULT_QUIT_BUTTON_WIDTH = 210
DEFAULT_QUIT_BUTTON_HEIGHT = 80
DEFAULT_QUIT_FONT = 36
QUIT_HOVER_GROWTH = 10

# Game Over Buttons
DEFAULT_BUTTON3_WIDTH = 250
DEFAULT_BUTTON3_HEIGHT = 90
DEFAULT_BUTTON3_MARGE = 80
DEFAULT_BUTTON3_MIN_WIDTH = 50
DEFAULT_BUTTON3_MIN_HEIGHT = 12
DEFAULT_BUTTON3_MIN_MARGE = 5

# Score
DEFAULT_SCORE_WIDTH = 200
DEFAULT_SCORE_HEIGHT = 125
DEFAULT_SCORE_MIN_WIDTH = 25
DEFAULT_SCORE_MIN_HEIGHT = 6

# Result
DEFAULT_RESULT_WIDTH = 800
DEFAULT_RESULT_HEIGHT = 300
DEFAULT_RESULT_MIN_WIDTH = 50
DEFAULT_RESULT_MIN_HEIGHT = 12

# Pixels
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

# Fonts
DEFAULT_MENU_FONT = 64
DEFAULT_GAME_OVER_FONT = 32
DEFAULT_TITLE_FONT = 112
DEFAULT_SCORE_FONT = 32
DEFAULT_RETURN_FONT = 32
DEFAULT_EXTRA_FONT = 32

# Menu States
MENUS = {
    "PRINCIPAL": [
        "SOLO",
        "VERSUS"
    ],
    "SELECT_PLAYER": [
        "P1 VS P2",
        "P1 VS IA"
    ],
    "SELECT_BOARD": [
        "1-BOARD",
        "2-BOARD"
    ],
    "DIFFICULTY": [
        "EASY",
        "NORMAL",
        "HARD",
        "INSANE"
    ],
    "GAME_OVER": [
        "TRY AGAIN",
        "MENU"
    ],
    "SETTINGS": [
        "SELECT SNAKE SKIN",
        "SELECT AMBIANCE SKIN",
        "EFFECTS VOLUME",
        "MUSIC VOLUME",
        "MUTE EFFECTS",
        "MUTE MUSIC"
    ],
    "SELECT_SKIN": [
        "P1 SKIN",
        "P2 SKIN"
    ]
}

POSSIBLE_EFFECTS = ["POISON", "FREEZE", "SPEED", "SCORE_UP", "SCORE_DOWN", "GROW"]

EFFECTS = {
    "SPEED" : {
        "duration" : 5,
        "boost": 0.75,
        "color": (253, 216, 8)
    }, 
    "SCORE_UP": {
        "duration" : 1,
        "boost" : 5,
        "color": (8, 146, 208)
    }, 
    "GROW" : {
        "duration" : 5,
        "boost" : 1,
        "color": (106, 13, 173)
    },
    "POISON": {
        "duration" : 1,
        "boost": -1,
        "color": (121, 6, 4)
    }, 
    "FREEZE": {
        "duration" : 5,
        "boost": 1.5,
        "color": (214, 234, 240)
    }, 
    "SCORE_DOWN": {
        "duration" : 1,
        "boost": -5,
        "color": (255, 69, 0)
    }
}

# Difficulties
EASY = {
    "name": "EASY",
    "grid_size": 10,
    "move_interval": 0.4,
    "max_food": 3,
    "food_interval": 33,
    "max_obstacles": 5,
    "max_power_up": 1,
    "power_up_interval": 0
}

NORMAL = {
    "name": "NORMAL",
    "grid_size": 20,
    "move_interval": 0.3,
    "max_food": 4,
    "food_interval": 100,
    "max_obstacles": 7,
    "max_power_up": 2,
    "power_up_interval": 100
}

HARD = {
    "name": "HARD",
    "grid_size": 30,
    "move_interval": 0.2,
    "max_food": 5,
    "food_interval": 180,
    "max_obstacles": 10,
    "max_power_up": 3,
    "power_up_interval": 300
}

ULTRA_HARD = {
    "name": "ULTRA_HARD",
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
# GRID_COLOR = (5, 2, 3)
# SNAKE_COLOR = (1, 50, 32)
# FOOD_COLOR = (118, 205, 38)
# MENU_COLOR = (0, 0, 0)
# MENU_HOVER_COLOR = (40, 40, 40)
# TEXT_COLOR = (255, 255, 255)
# TEXT_HOVER_COLOR = (255, 238, 140)
# SCORE_COLOR = (0, 0, 0)
# OBSTACLES_COLOR = (5, 2, 3)
# POISON_COLOR = (121, 6, 4)
# SPEED_COLOR = (253, 216, 8)
# SCORE_UP_COLOR = (8, 146, 208)
# BONUS_COLOR = (106, 13, 173)

TITLE_COLOR = (70, 59, 42)
SCORE_COLOR = (68, 97, 97)
BUTTON_COLOR = (47, 79, 79)
TEXT_HOVER_COLOR = (255, 238, 140)

# Fps
FPS = 60

# Controls
SOLO_CONTROLS = {
    pygame.K_UP: "UP",
    pygame.K_z: "UP",
    pygame.K_o: "UP",
    pygame.K_LEFT: "LEFT",
    pygame.K_q: "LEFT",
    pygame.K_k: "LEFT",
    pygame.K_DOWN: "DOWN",
    pygame.K_s: "DOWN",
    pygame.K_l: "DOWN",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_d: "RIGHT",
    pygame.K_m: "RIGHT"
}

MULTI_P1_CONTROLS = {
    pygame.K_z: "UP",
    pygame.K_q: "LEFT",
    pygame.K_s: "DOWN",
    pygame.K_d: "RIGHT"
}

MULTI_P2_CONTROLS = {
    pygame.K_UP: "UP",
    pygame.K_o: "UP",
    pygame.K_LEFT: "LEFT",
    pygame.K_k: "LEFT",
    pygame.K_DOWN: "DOWN",
    pygame.K_l: "DOWN",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_m: "RIGHT"
}

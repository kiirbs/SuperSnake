import pygame

PLAYER_1 = None

PLAYER_2 = None

HEAD_RIGHT = None
HEAD_UP = None
HEAD_LEFT = None
HEAD_DOWN = None

BODY_RIGHT = None
BODY_UP = None
BODY_LEFT = None
BODY_DOWN = None

BODY_L_DOWN = None
BODY_L_RIGHT = None
BODY_L_UP = None
BODY_L_LEFT = None

BODY_R_UP = None
BODY_R_LEFT = None
BODY_R_DOWN = None
BODY_R_RIGHT = None

TAIL_RIGHT = None
TAIL_UP = None
TAIL_LEFT = None
TAIL_DOWN = None

FLOOR = None
BACKGROUND = None
SET_UP = None
SET_UP_RIGHT =  None
SET_UP_LEFT =  None
SET_DOWN = None
SET_DOWN_RIGHT = None
SET_DOWN_LEFT = None
SET_RIGHT = None
SET_LEFT = None

BUTTON = None
BUTTON_HOVER = None
BUTTON_SELECT = None

BUTTON_2 = None
BUTTON_2_HOVER = None
BUTTON_2_SELECT = None

BUTTON_ON = None
BUTTON_OFF = None
GAUGE_BAR = None
GAUGE = None
CURSOR = None
SETTINGS_ICON = None
SETTINGS_ICON_HOVER = None

SCREEN = None
LARGE_SCREEN = None
SCREEN_3 = None
BANNER_SCREEN = None

FOOD = None
OBSTACLE = None
POWERUPS = None

PLAYER_SKINS = {
    "CLASSIC": {
        "HEAD": "assets/images/snake/head_1.png",
        "BODY": "assets/images/snake/body_1.png",
        "BODY_RIGHT": "assets/images/snake/body_1_right.png",
        "BODY_LEFT": "assets/images/snake/body_1_left.png",
        "TAIL": "assets/images/snake/tail_1.png"
    },
    "GEAR": {
        "HEAD": "assets/images/snake/head_2.png",
        "BODY_1": "assets/images/snake/body_2-1.png",
        "BODY_2": "assets/images/snake/body_2-2.png",
        "BODY_TURN": "assets/images/snake/body_2_turn.png",
        "TAIL": "assets/images/snake/tail_2.png"
    },
    "SKIN_3": {
        "HEAD": "assets/images/snake/head_3.png",
        "BODY": "assets/images/snake/body_3.png",
        "BODY_TURN": "assets/images/snake/body_3_turn.png",
        "TAIL": "assets/images/snake/tail_3.png"
    },
    "SKIN_4": {
        "HEAD": "assets/images/snake/head_4.png",
        "BODY": "assets/images/snake/body_4.png",
        "BODY_TURN": "assets/images/snake/body_4_turn.png",
        "TAIL": "assets/images/snake/tail_4.png"
    }
}

BOT_SKINS = {
    "CLASSIC": {
        "HEAD": "assets/images/snake/head_bot_1.png",
        "BODY": "assets/images/snake/body_bot_1.png",
        "BODY_TURN": "assets/images/snake/body_bot_turn_1.png",
        "TAIL": "assets/images/snake/tail_bot_1.png"
    },
    "UPGRADE": {
        "HEAD": "assets/images/snake/head_bot_2.png",
        "BODY": "assets/images/snake/body_bot_2.png",
        "BODY_TURN": "assets/images/snake/body_bot_turn_2.png",
        "TAIL": "assets/images/snake/tail_bot_2.png"
    }
}

# Les chemins restent dans les catalogues ; les surfaces sont chargees ici.
PLAYER_SKIN_ASSETS = {}
BOT_SKIN_ASSETS = {}


def load_skin(paths):
    """Charge un skin et prepare les orientations sans lisser les pixels."""
    sprites = {
        part: pygame.image.load(path).convert_alpha()
        for part, path in paths.items()
    }

    left_turn = sprites.get("BODY_LEFT", sprites.get("BODY_TURN"))
    right_turn = sprites.get("BODY_RIGHT", sprites.get("BODY_TURN"))

    # Chaque sprite droit est dessine vers la droite dans les fichiers sources.
    for part in ("HEAD", "BODY", "BODY_1", "BODY_2", "TAIL"):
        if part in sprites:
            for direction, angle in (("RIGHT", 0), ("UP", 90),
                                     ("LEFT", 180), ("DOWN", 270)):
                sprites[f"{part}_{direction}"] = pygame.transform.rotate(
                    sprites[part], angle
                )

    # CLASSIC possede deux virages distincts ; les autres partagent un virage.
    for prefix, sprite, directions in (
        ("BODY_L", left_turn, ("DOWN", "RIGHT", "UP", "LEFT")),
        ("BODY_R", right_turn, ("UP", "LEFT", "DOWN", "RIGHT")),
    ):
        for index, direction in enumerate(directions):
            sprites[f"{prefix}_{direction}"] = pygame.transform.rotate(
                sprite, index * 90
            )

    # GEAR garde ses deux variantes pour pouvoir alterner les segments.
    if "BODY" not in sprites:
        sprites["BODY"] = sprites["BODY_1"]
        for direction in ("RIGHT", "UP", "LEFT", "DOWN"):
            sprites[f"BODY_{direction}"] = sprites[f"BODY_1_{direction}"]

    return sprites

def load_assets():
    global SCREEN_3
    global BUTTON_ON, BUTTON_OFF, GAUGE_BAR, GAUGE, CURSOR
    global BUTTON_2, BUTTON_2_HOVER, BUTTON_2_SELECT

    global SETTINGS_ICON, SETTINGS_ICON_HOVER
    global HEAD_RIGHT, HEAD_UP, HEAD_LEFT, HEAD_DOWN, BODY_RIGHT, BODY_UP, BODY_LEFT, BODY_DOWN, BODY_L_DOWN, BODY_L_RIGHT, BODY_L_UP, BODY_L_LEFT, BODY_R_UP, BODY_R_LEFT, BODY_R_DOWN, BODY_R_RIGHT, TAIL_RIGHT, TAIL_UP, TAIL_LEFT, TAIL_DOWN, FOOD, OBSTACLE, FLOOR, BUTTON, BUTTON_HOVER, BUTTON_SELECT, POWERUPS, BACKGROUND, SCREEN, LARGE_SCREEN, BANNER_SCREEN, SET_DOWN, SET_DOWN_LEFT, SET_DOWN_RIGHT, SET_UP, SET_UP_LEFT, SET_UP_RIGHT, SET_LEFT, SET_RIGHT

    _scaled_cache.clear()
    PLAYER_SKIN_ASSETS.clear()
    BOT_SKIN_ASSETS.clear()
    for name, paths in PLAYER_SKINS.items():
        PLAYER_SKIN_ASSETS[name] = load_skin(paths)
    for name, paths in BOT_SKINS.items():
        BOT_SKIN_ASSETS[name] = load_skin(paths)

    # Compatibilite avec snake.py : le jeu utilise encore le skin CLASSIC.
    classic = PLAYER_SKIN_ASSETS["CLASSIC"]
    HEAD_RIGHT = classic["HEAD_RIGHT"]
    HEAD_UP = classic["HEAD_UP"]
    HEAD_LEFT = classic["HEAD_LEFT"]
    HEAD_DOWN = classic["HEAD_DOWN"]
    BODY_RIGHT = classic["BODY_RIGHT"]
    BODY_UP = classic["BODY_UP"]
    BODY_LEFT = classic["BODY_LEFT"]
    BODY_DOWN = classic["BODY_DOWN"]
    BODY_L_DOWN = classic["BODY_L_DOWN"]
    BODY_L_RIGHT = classic["BODY_L_RIGHT"]
    BODY_L_UP = classic["BODY_L_UP"]
    BODY_L_LEFT = classic["BODY_L_LEFT"]
    BODY_R_UP = classic["BODY_R_UP"]
    BODY_R_LEFT = classic["BODY_R_LEFT"]
    BODY_R_DOWN = classic["BODY_R_DOWN"]
    BODY_R_RIGHT = classic["BODY_R_RIGHT"]
    TAIL_RIGHT = classic["TAIL_RIGHT"]
    TAIL_UP = classic["TAIL_UP"]
    TAIL_LEFT = classic["TAIL_LEFT"]
    TAIL_DOWN = classic["TAIL_DOWN"]

    FLOOR = pygame.image.load("assets/images/ambiance/floor.png").convert_alpha()
    BACKGROUND = pygame.image.load("assets/images/ambiance/wall.png").convert()
    SET_UP = pygame.image.load("assets/images/ambiance/set_up.png").convert_alpha()
    SET_UP_RIGHT =  pygame.image.load("assets/images/ambiance/set_up_right.png").convert_alpha()
    SET_UP_LEFT =  pygame.image.load("assets/images/ambiance/set_up_left.png").convert_alpha()
    SET_DOWN = pygame.image.load("assets/images/ambiance/set_down.png").convert_alpha()
    SET_DOWN_RIGHT = pygame.image.load("assets/images/ambiance/set_down_right.png").convert_alpha()
    SET_DOWN_LEFT = pygame.image.load("assets/images/ambiance/set_down_left.png").convert_alpha()
    SET_RIGHT = pygame.image.load("assets/images/ambiance/set_right.png").convert_alpha()
    SET_LEFT = pygame.image.load("assets/images/ambiance/set_left.png").convert_alpha()
    
    BUTTON = pygame.image.load("assets/images/ui/button_1.png").convert_alpha()
    BUTTON_HOVER = pygame.image.load("assets/images/ui/button_1_hover.png").convert_alpha()
    BUTTON_SELECT = pygame.image.load("assets/images/ui/button_1_selected.png").convert_alpha()
    BUTTON_2 = pygame.image.load("assets/images/ui/button_2.png").convert_alpha()
    BUTTON_2_HOVER = pygame.image.load("assets/images/ui/button_2_hover.png").convert_alpha()
    BUTTON_2_SELECT = pygame.image.load("assets/images/ui/button_2_selected.png").convert_alpha()
    BUTTON_ON = pygame.image.load("assets/images/ui/button_on.png").convert_alpha()
    BUTTON_OFF = pygame.image.load("assets/images/ui/button_off.png").convert_alpha()
    GAUGE_BAR = pygame.image.load("assets/images/ui/gauge_bar.png").convert_alpha()
    GAUGE = pygame.image.load("assets/images/ui/gauge.png").convert_alpha()
    CURSOR = pygame.image.load("assets/images/ui/cursor.png").convert_alpha()
    SETTINGS_ICON = pygame.image.load("assets/images/ui/settings.png").convert_alpha()
    SETTINGS_ICON_HOVER = pygame.image.load("assets/images/ui/settings_hover.png").convert_alpha()
    
    SCREEN = pygame.image.load("assets/images/ui/screen_1.png").convert_alpha()
    LARGE_SCREEN = pygame.image.load("assets/images/ui/screen_2.png").convert_alpha()
    SCREEN_3 = pygame.image.load("assets/images/ui/screen_3.png").convert_alpha()
    BANNER_SCREEN = pygame.image.load("assets/images/ui/banner.png").convert_alpha()

    FOOD = pygame.image.load("assets/images/food/food.png").convert_alpha()
    OBSTACLE = pygame.image.load("assets/images/obstacle/obstacle.png").convert_alpha()
    POWERUPS = {
        "POISON": pygame.image.load("assets/images/powerup/poison_powerup.png").convert_alpha(),
        "SCORE_DOWN": pygame.image.load("assets/images/powerup/score_down_powerup.png").convert_alpha(),
        "SCORE_UP": pygame.image.load("assets/images/powerup/score_up_powerup.png").convert_alpha(),
        "FREEZE": pygame.image.load("assets/images/powerup/freeze_powerup.png").convert_alpha(),
        "SPEED": pygame.image.load("assets/images/powerup/speed_powerup.png").convert_alpha(),
        "GROW": pygame.image.load("assets/images/powerup/grow_powerup.png").convert_alpha()
    }

_scaled_cache = {}

def get_sprite(sprite, width, height=None):
    
    if height is None:
        height = width
        
    key = (id(sprite), width, height)
    
    if key not in _scaled_cache:
        _scaled_cache[key] = pygame.transform.scale(
            sprite,
            (width, height)
        )
        
    return _scaled_cache[key]

def create_font(size, scale):
    
    size = max(6, int(size * scale))
    
    return pygame.font.Font(
        "assets/fonts/FantasyRPGtext.ttf",
        size
    )

def create_hover_font(size, scale):
    
    size = max(6, int(size * scale * 1.1))
    
    return pygame.font.Font(
        "assets/fonts/FantasyRPGtext.ttf",
        size
    )
    
def print_asset(screen, image, cell_size, x, y):
    
    sprite = get_sprite(image, cell_size)
    
    if sprite is not None:
        screen.blit(sprite, (x, y))

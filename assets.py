import pygame

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

FOOD = None

OBSTACLE = None

FLOOR = None

BUTTON = None
BUTTON_HOVER = None
BUTTON_SELECT = None

POWERUPS = None

def load_assets():
    
    global HEAD_RIGHT, HEAD_UP, HEAD_LEFT, HEAD_DOWN, BODY_RIGHT, BODY_UP, BODY_LEFT, BODY_DOWN, BODY_L_DOWN, BODY_L_RIGHT, BODY_L_UP, BODY_L_LEFT, BODY_R_UP, BODY_R_LEFT, BODY_R_DOWN, BODY_R_RIGHT, TAIL_RIGHT, TAIL_UP, TAIL_LEFT, TAIL_DOWN, FOOD, OBSTACLE, FLOOR, BUTTON, BUTTON_HOVER, BUTTON_SELECT, POWERUPS
    
    HEAD_RIGHT = pygame.image.load("assets/images/snake/head_1.png").convert_alpha()
    HEAD_UP = pygame.transform.rotate(
        HEAD_RIGHT,
        90
    )
    HEAD_LEFT = pygame.transform.rotate(
        HEAD_UP,
        90
    )
    HEAD_DOWN = pygame.transform.rotate(
        HEAD_LEFT,
        90
    )

    BODY_RIGHT = pygame.image.load("assets/images/snake/body_1.png").convert_alpha()
    BODY_UP = pygame.transform.rotate(
        BODY_RIGHT,
        90
    )
    BODY_LEFT = pygame.transform.rotate(
        BODY_UP,
        90
    )
    BODY_DOWN = pygame.transform.rotate(
        BODY_LEFT,
        90
    )

    BODY_L_DOWN = pygame.image.load("assets/images/snake/body_1_left.png").convert_alpha()
    BODY_L_RIGHT = pygame.transform.rotate(
        BODY_L_DOWN,
        90
    )
    BODY_L_UP = pygame.transform.rotate(
        BODY_L_RIGHT,
        90
    )
    BODY_L_LEFT = pygame.transform.rotate(
        BODY_L_UP,
        90
    )

    BODY_R_UP = pygame.image.load("assets/images/snake/body_1_right.png").convert_alpha()
    BODY_R_LEFT = pygame.transform.rotate(
        BODY_R_UP,
        90
    )
    BODY_R_DOWN = pygame.transform.rotate(
        BODY_R_LEFT,
        90
    )
    BODY_R_RIGHT = pygame.transform.rotate(
        BODY_R_DOWN,
        90
    )

    TAIL_RIGHT = pygame.image.load("assets/images/snake/tail_1.png").convert_alpha()
    TAIL_UP = pygame.transform.rotate(
        TAIL_RIGHT,
        90
    )
    TAIL_LEFT = pygame.transform.rotate(
        TAIL_UP,
        90
    )
    TAIL_DOWN = pygame.transform.rotate(
        TAIL_LEFT,
        90
    )

    FOOD = pygame.image.load("assets/images/food/food.png").convert_alpha()

    OBSTACLE = pygame.image.load("assets/images/obstacle/obstacle.png").convert_alpha()
    
    FLOOR = pygame.image.load("assets/images/floor/floor.png").convert_alpha()
    
    BUTTON = pygame.image.load("assets/images/ui/button_1.png").convert_alpha()
    BUTTON_HOVER = pygame.image.load("assets/images/ui/button_1_hover.png").convert_alpha()
    BUTTON_SELECT = pygame.image.load("assets/images/ui/button_1_selected.png").convert_alpha()

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
import pygame

pygame.mixer.init()

CLICK_SOUND = pygame.mixer.Sound(
    "assets/sounds/click.ogg"
)

LOSE_SOUND = pygame.mixer.Sound(
    "assets/sounds/lose.mp3"
)

WIN_SOUND = pygame.mixer.Sound(
    "assets/sounds/win.mp3"
)

FOOD_SOUND = pygame.mixer.Sound(
    "assets/sounds/food.ogg"
)

POISON_SOUND = pygame.mixer.Sound(
    "assets/sounds/poison.ogg"
)

POWERUP_SOUND = pygame.mixer.Sound(
    "assets/sounds/powerup.ogg"
)
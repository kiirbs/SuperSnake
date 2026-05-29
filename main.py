import pygame
import random

# Setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
move_timer = 0

width = screen.get_width()
height = screen.get_height()

grid_size = 10
cell_size = min(width, height) // grid_size

BACKGROUND_COLOR = (58, 58, 58)
GRID_COLOR = (5, 2, 3)
SNAKE_COLOR = (0, 128, 0)
FOOD_COLOR = (121, 6, 4)

snake_head = [
    random.randint(2, grid_size - 3), 
    random.randint(2, grid_size - 3)
]
direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and direction != "DOWN":
                direction = "UP"
            
            elif event.key == pygame.K_s and direction != "UP":
                direction = "DOWN"
                
            elif event.key == pygame.K_q and direction != "RIGHT":
                direction = "LEFT"
                
            elif event.key == pygame.K_d and direction != "LEFT":
                direction = "RIGHT"
            
    screen.fill(BACKGROUND_COLOR)
    
    grid_offset_x = (width - grid_size * cell_size) / 2
    grid_offset_y = (height - grid_size * cell_size) / 2

    
    for row in range(grid_size):
        for col in range(grid_size):
            
            x = grid_offset_x + col * cell_size
            y = grid_offset_y + row * cell_size
            
            pygame.draw.rect(screen, GRID_COLOR, (x, y, cell_size, cell_size), 1)
            
    snake_row = snake_head[0]
    snake_col = snake_head[1]
            
    pygame.draw.rect(
        screen, 
        SNAKE_COLOR, 
        (
            grid_offset_x + snake_row * cell_size, 
            grid_offset_y + snake_col * cell_size, 
            cell_size - 1, 
            cell_size - 1
        )
    )
                
    move_timer += dt
    
    if move_timer >= 0.2:
        
        move_timer = 0
                
        if direction == "UP":
            snake_head[1] -= 1
        elif direction == "DOWN":
            snake_head[1] += 1
        elif direction == "LEFT":
            snake_head[0] -= 1
        elif direction == "RIGHT":
            snake_head[0] += 1
        
    if (
        snake_head[0] < 0 
        or snake_head[0] >= grid_size 
        or snake_head[1] < 0 
        or snake_head[1] >= grid_size
    ):
        running = False
    
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()
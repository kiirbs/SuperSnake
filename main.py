import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

width = screen.get_width()
height = screen.get_height()

grid_size = 10
cell_size = min(width, height) // grid_size

BACKGROUND_COLOR = (58, 58, 58)
GRID_COLOR = (5, 2, 3)
SNAKE_COLOR = (0, 128, 0)
FOOD_COLOR = (121, 6, 4)

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(BACKGROUND_COLOR)
    
    grid_offset_x = (width - grid_size * cell_size) / 2
    grid_offset_y = (height - grid_size * cell_size) / 2

    
    for row in range(grid_size):
        for col in range(grid_size):
            
            if width > height:
                x = grid_offset_x + col * cell_size
                y = grid_offset_y + row * cell_size
            
            pygame.draw.rect(screen, GRID_COLOR, (x, y, cell_size, cell_size), 1)
    
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()
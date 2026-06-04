import pygame

import settings

def draw_menu(screen, width, height):
    
    mouse_pos = pygame.mouse.get_pos()
    
    buttons = []
    
    difficult_len = len(settings.DIFFICULT)
    
    dw = width / settings.DEFAULT_WIDTH
    dh = height / settings.DEFAULT_HEIGHT
        
    button_width = max(100, int(settings.DEFAULT_BUTTON_WIDTH * dw))
    button_height = max(25, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    button_offset = max(3, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
    base_font_size = max(3, int(settings.DEFAULT_MENU_FONT * dh))
    menu_font = pygame.font.Font(None, base_font_size)
    hover_font = pygame.font.Font(None, int(base_font_size * 1.1))
    
    menu_width = button_width
    menu_height = ((
        difficult_len * button_height) 
        + ((difficult_len - 1) * button_offset
    ))
    offset = button_height + button_offset
    
    x = (width - menu_width) // 2
    y = (height - menu_height) // 2
        
    for button_text in settings.DIFFICULT:
        
        button_rect = pygame.Rect(
            x, 
            y,
            button_width, 
            button_height
        )
                
        if button_rect.collidepoint(mouse_pos):
            color = settings.MENU_HOVER_COLOR
            text_color = settings.TEXT_HOVER_COLOR
            font = hover_font
                        
            button_rect = pygame.Rect(
                x - 5,
                y - 5,
                button_width + 10,
                button_height + 10
            )
        else:
            color = settings.MENU_COLOR
            text_color = settings.TEXT_COLOR
            font = menu_font
        
        buttons.append((button_text, button_rect))

        text_surface = font.render(
            button_text,
            True,
            text_color
        )
        
        pygame.draw.rect(
            screen,
            color,
            button_rect,
        )
        
        text_rect = text_surface.get_rect(
            center=button_rect.center
        )
        
        screen.blit(text_surface, text_rect)
        
        y += offset
        
    return buttons

def draw_game_over(screen, width, height):
    
    mouse_pos = pygame.mouse.get_pos()
    
    buttons = []
    
    dw = width / settings.DEFAULT_WIDTH
    dh = height / settings.DEFAULT_HEIGHT
    
    button_width = max(50, int(settings.DEFAULT_BUTTON_WIDTH / 1.5 * dw))
    button_height = max(12, int(settings.DEFAULT_BUTTON_HEIGHT / 1.5 * dh))
    button_offset = max(3, int(settings.DEFAULT_BUTTON_MARGE * 4 * dh))
    
    button_pos = int(width / (len(settings.GAME_OVER) + 1))
    
    base_font_size = max(3, int(settings.DEFAULT_GAME_OVER_FONT * dh))
    menu_font = pygame.font.Font(None, base_font_size)
    hover_font = pygame.font.Font(None, int(base_font_size * 1.1))
    
    x = int(button_pos - (button_width / 2))
    y = height - (button_offset + button_height)
    
    for button_text in settings.GAME_OVER:
        
        button_rect = pygame.Rect(
            x, 
            y,
            button_width, 
            button_height
        )
        
        if button_rect.collidepoint(mouse_pos):
            color = settings.MENU_HOVER_COLOR
            text_color = settings.TEXT_HOVER_COLOR
            font = hover_font
                        
            button_rect = pygame.Rect(
                x - 5,
                y - 5,
                button_width + 10,
                button_height + 10
            )
        else:
            color = settings.MENU_COLOR
            text_color = settings.TEXT_COLOR
            font = menu_font
            
        buttons.append((button_text, button_rect))

        text_surface = font.render(
            button_text,
            True,
            text_color
        )
        
        pygame.draw.rect(
            screen,
            color,
            button_rect,
        )
        
        text_rect = text_surface.get_rect(
            center=button_rect.center
        )
        
        screen.blit(text_surface, text_rect)
        
        x += button_pos
        
    return buttons

def print_game_result(screen, game_result, width, height):
    
    dh = height / settings.DEFAULT_HEIGHT
    
    button_height = max(12, int(settings.DEFAULT_BUTTON_HEIGHT / 1.5 * dh))
    button_offset = max(3, int(settings.DEFAULT_BUTTON_MARGE * 4 * dh))
    
    y = button_offset + button_height
    
    base_font_size = max(3, int(settings.DEFAULT_TITLE_FONT * dh))
    font = pygame.font.Font(None, base_font_size)

    text_surface = font.render(
        game_result,
        True,
        settings.TEXT_COLOR
    )
    
    text_rect = text_surface.get_rect(
        center=(width // 2, (height - y) // 2)
    )
    
    screen.blit(text_surface, text_rect)
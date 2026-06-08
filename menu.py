import pygame
from collections import deque

import settings

def get_scale(width, height):
    
    dw = width / settings.DEFAULT_WIDTH
    dh = height / settings.DEFAULT_HEIGHT
    
    return dw, dh

def create_font(font_size, dh):
    
    base_font_size = max(3, int(font_size * dh))
    item_font = pygame.font.Font(None, base_font_size)
    hover_font = pygame.font.Font(None, int(base_font_size * 1.1))
    
    return item_font, hover_font

def draw_menu(screen, width, height, states):
    
    mouse_pos = pygame.mouse.get_pos()
    
    buttons = deque([])
    
    states_len = len(states)
    
    dw, dh = get_scale(width, height)
        
    button_width = max(100, int(settings.DEFAULT_BUTTON_WIDTH * dw))
    button_height = max(25, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    button_offset = max(3, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
    menu_font, hover_font = create_font(settings.DEFAULT_MENU_FONT, dh)
    
    menu_width = button_width
    menu_height = (
        (states_len * button_height) 
        + ((states_len - 1) * button_offset)
    )
    offset = button_height + button_offset
    
    x = (width - menu_width) // 2
    y = 125 + ((height - menu_height) // 2)
        
    for button_text in states:
        
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
    
    buttons = deque([])
    
    dw, dh = get_scale(width, height)
    
    button_width = max(settings.DEFAULT_BUTTON3_MIN_WIDTH, int(settings.DEFAULT_BUTTON3_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON3_MIN_HEIGHT, int(settings.DEFAULT_BUTTON3_HEIGHT * dh))
    button_offset = max(settings.DEFAULT_BUTTON3_MIN_MARGE, int(settings.DEFAULT_BUTTON3_MARGE * dh))
    
    menu_font, hover_font = create_font(settings.DEFAULT_GAME_OVER_FONT, dh)
    
    button_pos = int(width / (len(settings.GAME_OVER) + 1))
    
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
    
    button_height = max(12, int(settings.DEFAULT_BUTTON3_HEIGHT * dh))
    button_offset = max(5, int(settings.DEFAULT_BUTTON3_MARGE * dh))
    
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
    
def draw_return(screen, width, height):
    
    mouse_pos = pygame.mouse.get_pos()
    
    dw, dh = get_scale(width, height)
    
    button_width = max(settings.DEFAULT_BUTTON2_MIN_WIDTH, int(settings.DEFAULT_BUTTON2_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON2_MIN_HEIGHT, int(settings.DEFAULT_BUTTON2_HEIGHT * dh))
    
    menu_font, hover_font = create_font(settings.DEFAULT_RETURN_FONT, dh)
    
    x = width - ((50 * dw) + button_width)
    y = height - ((30 * dh) + button_height)
    
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
        
    text_surface = font.render(
        "RETURN",
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
    
    return ("RETURN", button_rect)
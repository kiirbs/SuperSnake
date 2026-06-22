import pygame
from collections import deque

import game
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
        
    button_width = max(settings.DEFAULT_BUTTON_MIN_WIDTH, int(settings.DEFAULT_BUTTON_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON_MIN_HEIGHT, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    button_offset = max(settings.DEFAULT_BUTTON_MIN_MARGE, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
    menu_font, hover_font = create_font(settings.DEFAULT_MENU_FONT, dh)
    
    menu_width = button_width
    menu_height = (
        (states_len * button_height) 
        + ((states_len - 1) * button_offset)
    )
    offset = button_height + button_offset
    
    x = (width - menu_width) // 2
    y = settings.DEFAULT_TITLE_MARGE + (((height - settings.DEFAULT_TITLE_MARGE) - menu_height) // 2)
        
    for button_text in states:
        
        button_rect = game.create_rect(x, y, button_width, button_height)
                
        if button_rect.collidepoint(mouse_pos):
            color = settings.MENU_HOVER_COLOR
            text_color = settings.TEXT_HOVER_COLOR
            font = hover_font
                 
            button_rect = game.create_rect(x - 5, y - 5, button_width + 10, button_height + 10)
            
        else:
            color = settings.MENU_COLOR
            text_color = settings.TEXT_COLOR
            font = menu_font
        
        buttons.append((button_text, button_rect))
        
        pygame.draw.rect(
            screen,
            color,
            button_rect,
        )
        
        text_surface, text_rect = game.create_text(font, button_text, text_color, button_rect)
        
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
        
        button_rect = game.create_rect(x, y, button_width, button_height)
        
        if button_rect.collidepoint(mouse_pos):
            color = settings.MENU_HOVER_COLOR
            text_color = settings.TEXT_HOVER_COLOR
            font = hover_font
                        
            button_rect = game.create_rect(x - 5, y - 5, button_width + 10, button_height + 10)
            
        else:
            color = settings.MENU_COLOR
            text_color = settings.TEXT_COLOR
            font = menu_font
            
        buttons.append((button_text, button_rect))
        
        pygame.draw.rect(
            screen,
            color,
            button_rect,
        )
        
        text_surface, text_rect = game.create_text(font, button_text, text_color, button_rect)
        
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
    
def draw_second_menu(screen, buttons, obstacle_mode, powerup_mode, width, height, states):
    
    mouse_pos = pygame.mouse.get_pos()
    
    states_len = len(states)
    
    dw, dh = get_scale(width, height)
    
    button_width = max(settings.DEFAULT_BUTTON2_MIN_WIDTH, int(settings.DEFAULT_BUTTON2_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON2_MIN_HEIGHT, int(settings.DEFAULT_BUTTON2_HEIGHT * dh))
    
    menu_height = max(settings.DEFAULT_BUTTON_MIN_HEIGHT, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    menu_offset = max(settings.DEFAULT_BUTTON_MIN_MARGE, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
    menu_font, hover_font = create_font(settings.DEFAULT_RETURN_FONT, dh)
    
    menu_height = (
        (states_len * menu_height)
        + ((states_len - 1) * menu_offset)
    )
    
    return_x = width - ((60 * dw) + button_width)
    extra_x = 60 * dw
    y = height - (((height - settings.DEFAULT_TITLE_MARGE) - menu_height) // 2) - button_height
    
    return_rect = game.create_rect(return_x, y, button_width, button_height)
    obstacle_rect = game.create_rect(extra_x, y, button_width, button_height)
    powerup_rect = game.create_rect(extra_x, y - int(10*dh) - button_height, button_width, button_height)
    
    if return_rect.collidepoint(mouse_pos):
        return_color = settings.MENU_HOVER_COLOR
        return_text_color = settings.TEXT_HOVER_COLOR
        return_font = hover_font
                        
        return_rect = game.create_rect(return_x - 5, y - 5, button_width + 10, button_height + 10)
        
    else:
        return_color = settings.MENU_COLOR
        return_text_color = settings.TEXT_COLOR
        return_font = menu_font
        
    if obstacle_rect.collidepoint(mouse_pos):
        obstacle_color = settings.MENU_HOVER_COLOR
        obstacle_text_color = settings.TEXT_HOVER_COLOR
        obstacle_font = hover_font
                        
        obstacle_rect = game.create_rect(extra_x - 5, y - 5, button_width + 10, button_height + 10)
        
    else:
        if obstacle_mode:
            obstacle_text_color = settings.TEXT_HOVER_COLOR
        else:
            obstacle_text_color = settings.TEXT_COLOR
            
        obstacle_color = settings.MENU_COLOR
        obstacle_font = menu_font
        
    if obstacle_mode:
        obstacle_text = "OBSTACLES : ON"
    else:
        obstacle_text = "OBSTACLES : OFF"
        
    if powerup_rect.collidepoint(mouse_pos):
        powerup_color = settings.MENU_HOVER_COLOR
        powerup_text_color = settings.TEXT_HOVER_COLOR
        powerup_font = hover_font
                        
        powerup_rect = game.create_rect(
            extra_x - 5, 
            y - int(10*dh) - button_height - 5, 
            button_width + 10, 
            button_height + 10)
        
    else:
        if powerup_mode:
            powerup_text_color = settings.TEXT_HOVER_COLOR
        else:
            powerup_text_color = settings.TEXT_COLOR
            
        powerup_color = settings.MENU_COLOR
        powerup_font = menu_font
        
    if powerup_mode:
        powerup_text = "POWER UP : ON"
    else:
        powerup_text = "POWER UP : OFF"
        
    pygame.draw.rect(
        screen,
        return_color,
        return_rect,
    )
    pygame.draw.rect(
        screen,
        obstacle_color,
        obstacle_rect,
    )
    pygame.draw.rect(
        screen,
        powerup_color,
        powerup_rect,
    )
    
    return_text_surface, return_text_rect = game.create_text(return_font, "RETURN", return_text_color, return_rect)
    obstacle_text_surface, obstacle_text_rect = game.create_text(obstacle_font, obstacle_text, obstacle_text_color, obstacle_rect)
    powerup_text_surface, powerup_text_rect = game.create_text(powerup_font, powerup_text, powerup_text_color, powerup_rect)
        
    screen.blit(return_text_surface, return_text_rect)
    screen.blit(obstacle_text_surface, obstacle_text_rect)
    screen.blit(powerup_text_surface, powerup_text_rect)
    
    buttons.append(("RETURN", return_rect))
    buttons.append(("OBSTACLE", obstacle_rect))
    buttons.append(("POWERUP", powerup_rect))
    
    return buttons
import pygame
from collections import deque

import game
import assets
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

def draw_button(screen, rect, text, sprite, font, text_color):
    
    lines = text.split("\n")
    
    line_height = font.get_height()
    total_height = len(lines) * line_height
    
    button_sprite = assets.get_sprite(
            sprite,
            rect.width,
            rect.height
        )
    screen.blit(button_sprite, rect)
    
    start_y = rect.centery - total_height // 2
    
    for i, line in enumerate(lines):
        surface = font.render(line, True, text_color)
        text_rect = surface.get_rect(
            center=(
                rect.centerx,
                start_y + i * line_height + line_height // 2
            )
        )
        screen.blit(surface, text_rect)

def draw_menu(screen, width, height, states, marge):
    
    mouse_pos = pygame.mouse.get_pos()
    
    buttons = deque([])
    
    states_len = len(states)
    
    dw, dh = get_scale(width, height)
        
    button_width = max(settings.DEFAULT_BUTTON_MIN_WIDTH, int(settings.DEFAULT_BUTTON_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON_MIN_HEIGHT, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    button_offset = max(settings.DEFAULT_BUTTON_MIN_MARGE, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
    # menu_font, hover_font = create_font(settings.DEFAULT_MENU_FONT, dh)
    menu_font = assets.create_font(settings.DEFAULT_MENU_FONT, dh)
    hover_font = assets.create_hover_font(settings.DEFAULT_MENU_FONT, dh)
    
    menu_width = button_width
    menu_height = (
        (states_len * button_height) 
        + ((states_len - 1) * button_offset)
    )
    offset = button_height + button_offset
    
    x = (width - menu_width) // 2
    y = marge + (((height - marge) - menu_height) // 2)
        
    for button_text in states:
        
        button_rect = game.create_rect(x, y, button_width, button_height)
                
        if button_rect.collidepoint(mouse_pos):
            sprite = assets.BUTTON_HOVER
            text_color = settings.TEXT_HOVER_COLOR
            font = hover_font
                 
            button_rect = game.create_rect(x - 5, y - 5, button_width + 10, button_height + 10)
            
        else:
            sprite = assets.BUTTON
            text_color = settings.TEXT_COLOR
            font = menu_font
        
        buttons.append((button_text, button_rect))
        
        draw_button(screen, button_rect, button_text, sprite, font, text_color)
        
        y += offset
        
    return buttons

def draw_game_over(screen, width, height, options):
    
    mouse_pos = pygame.mouse.get_pos()
    
    buttons = deque([])
    
    dw, dh = get_scale(width, height)
    
    button_width = max(settings.DEFAULT_BUTTON3_MIN_WIDTH, int(settings.DEFAULT_BUTTON3_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON3_MIN_HEIGHT, int(settings.DEFAULT_BUTTON3_HEIGHT * dh))
    button_offset = max(settings.DEFAULT_BUTTON3_MIN_MARGE, int(settings.DEFAULT_BUTTON3_MARGE * dh))
    
    # menu_font, hover_font = create_font(settings.DEFAULT_GAME_OVER_FONT, dh)
    menu_font = assets.create_font(settings.DEFAULT_GAME_OVER_FONT, dh)
    hover_font = assets.create_hover_font(settings.DEFAULT_GAME_OVER_FONT, dh)
    
    button_pos = int(width / (len(options) + 1))
    
    x = int(button_pos - (button_width / 2))
    y = height - (button_offset + button_height)
    
    for button_text in options:
        
        button_rect = game.create_rect(x, y, button_width, button_height)
        
        if button_rect.collidepoint(mouse_pos):
            sprite = assets.BUTTON_HOVER
            text_color = settings.TEXT_HOVER_COLOR
            font = hover_font
                        
            button_rect = game.create_rect(x - 5, y - 5, button_width + 10, button_height + 10)
            
        else:
            sprite = assets.BUTTON
            text_color = settings.TEXT_COLOR
            font = menu_font
            
        buttons.append((button_text, button_rect))
        
        draw_button(screen, button_rect, button_text, sprite, font, text_color)
        
        x += button_pos
        
    return buttons

def print_game_result(screen, game_result, width, height):
    
    dh = height / settings.DEFAULT_HEIGHT
    
    button_height = max(12, int(settings.DEFAULT_BUTTON3_HEIGHT * dh))
    button_offset = max(5, int(settings.DEFAULT_BUTTON3_MARGE * dh))
    
    y = button_offset + button_height
    
    # base_font_size = max(3, int(settings.DEFAULT_TITLE_FONT * dh))
    # font = pygame.font.Font(None, base_font_size)
    
    font = assets.create_font(settings.DEFAULT_TITLE_FONT, dh)

    text_surface = font.render(
        game_result,
        True,
        settings.TEXT_COLOR
    )
    
    text_rect = text_surface.get_rect(
        center=(width // 2, (height - y) // 2)
    )
    
    screen.blit(text_surface, text_rect)
    
def second_menu_setup(states, width, height, marge):
    
    mouse_pos = pygame.mouse.get_pos()
    
    states_len = len(states)
    
    dw, dh = get_scale(width, height)
    
    button_width = max(settings.DEFAULT_BUTTON2_MIN_WIDTH, int(settings.DEFAULT_BUTTON2_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON2_MIN_HEIGHT, int(settings.DEFAULT_BUTTON2_HEIGHT * dh))
    
    menu_height = max(settings.DEFAULT_BUTTON_MIN_HEIGHT, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    menu_offset = max(settings.DEFAULT_BUTTON_MIN_MARGE, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
    # menu_font, hover_font = create_font(settings.DEFAULT_RETURN_FONT, dh)
    menu_font = assets.create_font(settings.DEFAULT_RETURN_FONT, dh)
    hover_font = assets.create_hover_font(settings.DEFAULT_RETURN_FONT, dh)
    
    menu_height = (
        (states_len * menu_height)
        + ((states_len - 1) * menu_offset)
    )
    
    menu_y = height - (((height - marge) - menu_height) // 2) - button_height
    
    return mouse_pos, dw, dh, button_width, button_height, menu_font, hover_font, menu_y

def get_button_statue(mouse_pos, rect, font, hover_font, extra_x, y, button_width, button_height, mode, text):
    
    if rect.collidepoint(mouse_pos):
        sprite = assets.BUTTON_HOVER
        text_color = settings.TEXT_HOVER_COLOR
        selected_font = hover_font
                        
        rect = game.create_rect(extra_x - 5, y - 5, button_width + 10, button_height + 10)
        
    else:
        text_color = settings.TEXT_HOVER_COLOR if mode else settings.TEXT_COLOR
        sprite = assets.BUTTON_SELECT if mode else assets.BUTTON 
        selected_font = font
        
    state = "ON" if mode else "OFF"
    text = f"{text}\n{state}"
        
    return rect, sprite, text_color, selected_font, text
    
def draw_second_menu(screen, buttons, obstacle_mode, powerup_mode, width, height, states, marge):
    
    mouse_pos, dw, dh, button_width, button_height, menu_font, hover_font, y = second_menu_setup(
        states,
        width,
        height,
        marge
    )
    
    return_x = width - ((60 * dw) + button_width)
    extra_x = 60 * dw
    
    return_rect = game.create_rect(return_x, y, button_width, button_height)
    obstacle_rect = game.create_rect(extra_x, y, button_width, button_height)
    powerup_rect = game.create_rect(extra_x, y - int(20*dh) - button_height, button_width, button_height)
    
    if return_rect.collidepoint(mouse_pos):
        return_sprite = assets.BUTTON_HOVER
        return_text_color = settings.TEXT_HOVER_COLOR
        return_font = hover_font
                        
        return_rect = game.create_rect(return_x - 5, y - 5, button_width + 10, button_height + 10)
        
    else:
        return_sprite = assets.BUTTON
        return_text_color = settings.TEXT_COLOR
        return_font = menu_font
        
    obstacle_rect, obstacle_sprite, obstacle_text_color, obstacle_font, obstacle_text = get_button_statue(
        mouse_pos, 
        obstacle_rect, 
        menu_font, 
        hover_font, 
        extra_x, 
        y, 
        button_width, 
        button_height, 
        obstacle_mode, 
        "OBSTACLES: "
    )
        
    powerup_rect, powerup_sprite, powerup_text_color, powerup_font, powerup_text = get_button_statue(
        mouse_pos, 
        powerup_rect, 
        menu_font, 
        hover_font, 
        extra_x, 
        y - int(10*dh) - button_height, 
        button_width, 
        button_height, 
        powerup_mode, 
        "POWER-UP: "
    )
    
    
    
    draw_button(screen, return_rect, "RETURN", return_sprite, return_font, return_text_color)
    draw_button(screen, obstacle_rect, obstacle_text, obstacle_sprite, obstacle_font, obstacle_text_color)
    draw_button(screen, powerup_rect, powerup_text, powerup_sprite, powerup_font, powerup_text_color)
    
    buttons.append(("RETURN", return_rect))
    buttons.append(("OBSTACLE", obstacle_rect))
    buttons.append(("POWERUP", powerup_rect))
    
    return buttons

# def draw_bot_menu(screen, buttons, bot_mode, width, height, states):
    
#     mouse_pos, dw, dh, button_width, button_height, menu_font, hover_font, y = second_menu_setup(
#         states,
#         width,
#         height
#     )
    
#     x = 60 * dw
#     y = y - int(40*dh) - (2 * button_height)
    
#     bot_rect = game.create_rect(x, y, button_width, button_height)
        
#     if bot_rect.collidepoint(mouse_pos):
#         bot_color = settings.MENU_HOVER_COLOR
#         bot_text_color = settings.TEXT_HOVER_COLOR
#         bot_font = hover_font
                        
#         bot_rect = game.create_rect(x - 5, y - 5, button_width + 10, button_height + 10)
        
#     else:
#         if bot_mode:
#             bot_text_color = settings.TEXT_HOVER_COLOR
#         else:
#             bot_text_color = settings.TEXT_COLOR
            
#         bot_color = settings.MENU_COLOR
#         bot_font = menu_font
        
#     if bot_mode:
#         bot_text = "BOT : ON"
#     else:
#         bot_text = "BOT : OFF"
        
#     pygame.draw.rect(
#         screen,
#         bot_color,
#         bot_rect,
#     )
    
#     bot_text_surface, bot_text_rect = game.create_text(bot_font, bot_text, bot_text_color, bot_rect)
        
#     screen.blit(bot_text_surface, bot_text_rect)
    
#     buttons.append(("BOT", bot_rect))
    
#     return buttons
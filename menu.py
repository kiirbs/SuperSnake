import pygame

import settings

def draw_menu(screen, width, height):
    
    buttons = []
    
    difficult_len = len(settings.DIFFICULT)
    
    dw = width / settings.DEFAULT_WIDTH
    dh = height / settings.DEFAULT_HEIGHT
        
    button_width = max(100, int(settings.DEFAULT_BUTTON_WIDTH * dw))
    button_height = max(25, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    button_offset = max(3, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
    menu_font = pygame.font.Font(None, max(3, int(settings.DEFAULT_MENU_FONT * dh)))
    
    menu_width = button_width
    menu_height = ((
        difficult_len * button_height) 
        + ((difficult_len - 1) * button_offset
    ))
    offset = button_height + button_offset
    
    x = (width - menu_width) // 2
    y = (height - menu_height) // 2
        
    for button_text in settings.DIFFICULT:
                
        text_surface = menu_font.render(
            button_text,
            True,
            settings.TEXT_COLOR
        )
        
        button_rect = pygame.Rect(
            x, 
            y,
            button_width, 
            button_height
        )
        
        buttons.append((button_text, button_rect))
        
        pygame.draw.rect(
            screen,
            settings.MENU_COLOR,
            button_rect,
        )
        
        text_rect = text_surface.get_rect(
            center=button_rect.center
        )
        
        screen.blit(text_surface, text_rect)
        
        y += offset
        
    return buttons
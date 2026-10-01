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
            text_color = settings.BUTTON_COLOR
            font = menu_font
        
        buttons.append((button_text, button_rect))
        
        draw_button(screen, button_rect, button_text, sprite, font, text_color)
        
        y += offset
        
    return buttons

def get_main_menu_bottom(height, dh, marge):
    """Calcule l'alignement commun des boutons lateraux du menu principal."""
    menu_button_height = max(settings.DEFAULT_BUTTON_MIN_HEIGHT, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    menu_button_offset = max(settings.DEFAULT_BUTTON_MIN_MARGE, int(settings.DEFAULT_BUTTON_MARGE * dh))
    states_len = len(settings.MENUS["PRINCIPAL"])
    menu_height = states_len * menu_button_height + (states_len - 1) * menu_button_offset
    menu_y = marge + (height - marge - menu_height) // 2
    return menu_y + menu_height


def draw_settings_button(screen, width, height, marge):
    dw, dh = get_scale(width, height)
    # Une echelle commune conserve la forme carree au redimensionnement.
    button_scale = min(dw, dh)
    button_width = max(1, int(settings.DEFAULT_SETTINGS_BUTTON_WIDTH * button_scale))
    button_height = max(1, int(settings.DEFAULT_SETTINGS_BUTTON_HEIGHT * button_scale))
    x = width - int(settings.DEFAULT_SETTINGS_BUTTON_MARGE * dw) - button_width
    menu_bottom = get_main_menu_bottom(height, dh, marge)
    # Le bas du bouton reste aligne sur le bas du menu, meme apres redimensionnement.
    y = menu_bottom - button_height
    rect = game.create_rect(x, y, button_width, button_height)

    if rect.collidepoint(pygame.mouse.get_pos()):
        sprite = assets.BUTTON_2_HOVER
        icon_sprite = assets.SETTINGS_ICON_HOVER
        # Meme agrandissement que les autres boutons, en gardant le bas aligne.
        rect = rect.inflate(settings.SETTINGS_HOVER_GROWTH, settings.SETTINGS_HOVER_GROWTH)
        rect.bottom = menu_bottom
    else:
        sprite = assets.BUTTON_2
        icon_sprite = assets.SETTINGS_ICON

    screen.blit(assets.get_sprite(sprite, rect.width, rect.height), rect)
    icon_size = max(1, int(rect.width * settings.SETTINGS_ICON_RATIO))
    icon = assets.get_sprite(icon_sprite, icon_size, icon_size)
    screen.blit(icon, icon.get_rect(center=rect.center))
    return rect


class SettingsMenu:
    """Etat visuel des reglages ; aucune modification du son ou des skins."""

    def __init__(self):
        self.volumes = {
            "EFFECTS VOLUME": settings.SETTINGS_DEFAULT_VOLUME,
            "MUSIC VOLUME": settings.SETTINGS_DEFAULT_VOLUME,
        }
        self.muted = {"MUTE EFFECTS": False, "MUTE MUSIC": False}
        self.dragging = None

    def get_pixel_rect(self, sprite, bounds):
        """Chaque pixel source devient un carre de taille entiere."""
        pixel_scale = max(1, min(
            bounds.width // sprite.get_width(),
            bounds.height // sprite.get_height(),
        ))
        result = pygame.Rect(0, 0,
            sprite.get_width() * pixel_scale, sprite.get_height() * pixel_scale)
        result.center = bounds.center
        return result

    def get_layout(self, width, height):
        # Une echelle commune garde les trois colonnes dans la fenetre.
        scale = min(width / settings.DEFAULT_WIDTH, height / settings.DEFAULT_HEIGHT)
        offset_x = (width - settings.DEFAULT_WIDTH * scale) / 2
        offset_y = (height - settings.DEFAULT_HEIGHT * scale) / 2

        def rect(x, y, w, h):
            return pygame.Rect(
                round(offset_x + x * scale), round(offset_y + y * scale),
                max(1, round(w * scale)), max(1, round(h * scale)),
            )

        controls = {}
        margin = settings.SETTINGS_MENU_MARGIN
        column_width = settings.SETTINGS_COLUMN_WIDTH
        row_height = settings.SETTINGS_ROW_HEIGHT
        column_rows = [0, 0, 0]
        column_x = (
            margin,
            (settings.DEFAULT_WIDTH - column_width) / 2,
            settings.DEFAULT_WIDTH - margin - column_width,
        )
        for label in settings.MENUS["SETTINGS"]:
            if label in self.muted:
                column = 0
            elif label in self.volumes:
                column = 1
            else:
                column = 2
            y = settings.SETTINGS_MENU_TOP + column_rows[column] * (
                row_height + settings.SETTINGS_ROW_GAP
            )
            bounds = rect(column_x[column], y, column_width, row_height)
            bounds.centerx = round(offset_x + (column_x[column] + column_width / 2) * scale)
            button_rect = self.get_pixel_rect(assets.BUTTON, bounds)
            if label in self.volumes:
                bounds.height += round(settings.SETTINGS_VOLUME_PANEL_EXTRA_HEIGHT * scale)
                bounds.centery = button_rect.centery
                controls[label] = self.get_pixel_rect(assets.LARGE_SCREEN, bounds)
            else:
                controls[label] = button_rect
            column_rows[column] += 1

        controls["RETURN"] = self.get_pixel_rect(
            assets.BUTTON, rect((settings.DEFAULT_WIDTH - 220) / 2, 610, 220, 84)
        )
        heading = rect(margin, 55, settings.DEFAULT_WIDTH - 2 * margin, 60)
        return controls, heading, scale

    def get_volume_frame(self, rect):
        return settings.SETTINGS_VOLUME_FRAME_SIZE * (rect.width // assets.LARGE_SCREEN.get_width())

    def get_volume_font(self, rect, scale):
        return assets.create_font(settings.SETTINGS_VOLUME_FONT, min(
            scale,
            rect.width / (assets.LARGE_SCREEN.get_width() * settings.SETTINGS_VOLUME_REFERENCE_PIXEL_SCALE),
        ))

    def get_slider_bar(self, rect, scale):
        frame = self.get_volume_frame(rect)
        font = self.get_volume_font(rect, scale)
        bar_height = max(1, min(round(settings.SETTINGS_SLIDER_HEIGHT * scale),
            rect.height - 2 * frame - 2 * font.get_height()))
        bounds = pygame.Rect(
            rect.left + frame,
            rect.bottom - max(frame, round(settings.SETTINGS_SLIDER_BOTTOM_MARGIN * scale)) - bar_height,
            max(1, rect.width - 2 * frame), bar_height,
        )
        return self.get_pixel_rect(assets.GAUGE_BAR, bounds)

    def get_slider_track(self, rect, scale):
        bar = self.get_slider_bar(rect, scale)
        # La zone coloree de gauge.png definit la course utile du curseur.
        # Ses marges transparentes restent alignees avec gauge_bar.png.
        fill = assets.GAUGE.get_bounding_rect()
        sprite_width, sprite_height = assets.GAUGE.get_size()
        return pygame.Rect(
            bar.left + round(fill.left * bar.width / sprite_width),
            bar.top + round(fill.top * bar.height / sprite_height),
            max(1, round(fill.width * bar.width / sprite_width)),
            max(1, round(fill.height * bar.height / sprite_height)),
        )

    def update_volume(self, label, mouse_x, controls, scale):
        track = self.get_slider_track(controls[label], scale)
        self.volumes[label] = max(0.0, min(1.0, (mouse_x - track.left) / track.width))

    def handle_event(self, event, width, height):
        """Renvoie True uniquement quand RETURN est clique."""
        controls, heading, scale = self.get_layout(width, height)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for label, rect in controls.items():
                if rect.collidepoint(event.pos):
                    if label in self.volumes:
                        self.dragging = label
                        self.update_volume(label, event.pos[0], controls, scale)
                    elif label in self.muted:
                        self.muted[label] = not self.muted[label]
                    return label == "RETURN"
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_volume(self.dragging, event.pos[0], controls, scale)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = None
        elif event.type == pygame.WINDOWFOCUSLOST:
            self.dragging = None
        return False

    def draw(self, screen, width, height):
        controls, heading, scale = self.get_layout(width, height)
        mouse_pos = pygame.mouse.get_pos()
        font = assets.create_font(settings.SETTINGS_MENU_FONT, scale)
        title_font = assets.create_font(settings.SETTINGS_HEADING_FONT, scale)
        title = title_font.render("SETTINGS", True, settings.SETTINGS_TEXT_COLOR)
        screen.blit(title, title.get_rect(center=heading.center))
        padding = max(1, round(12 * scale))

        for label, rect in controls.items():
            hovered = rect.collidepoint(mouse_pos) or self.dragging == label
            selected = self.muted.get(label, False)
            if label in self.volumes:
                text_color = settings.TEXT_HOVER_COLOR if hovered else settings.SETTINGS_TEXT_COLOR
                screen.blit(assets.get_sprite(assets.LARGE_SCREEN, rect.width, rect.height), rect)
            else:
                # Les textures passent par le chargement et le cache existants.
                sprite = assets.BUTTON_SELECT if selected else assets.BUTTON
                if hovered:
                    sprite = assets.BUTTON_HOVER
                text_color = settings.TEXT_HOVER_COLOR if hovered or selected else settings.BUTTON_COLOR
                if label in self.muted:
                    screen.blit(assets.get_sprite(sprite, rect.width, rect.height), rect)

            if label in self.volumes:
                volume_font = self.get_volume_font(rect, scale)
                frame = self.get_volume_frame(rect)
                # Deux lignes laissent la place a la jauge dans le cadre original.
                for index, text in enumerate((label, f"{round(self.volumes[label] * 100)}%")):
                    surface = volume_font.render(text, True, text_color)
                    screen.blit(surface, surface.get_rect(midtop=(
                        rect.centerx, rect.top + frame + index * volume_font.get_height(),
                    )))
                bar = self.get_slider_bar(rect, scale)
                track = self.get_slider_track(rect, scale)
                screen.blit(assets.get_sprite(assets.GAUGE_BAR, bar.width, bar.height), bar)
                pixel_scale = bar.width // assets.GAUGE_BAR.get_width()
                fill_width = round(assets.GAUGE.get_bounding_rect().width * self.volumes[label]) * pixel_scale
                if fill_width > 0:
                    gauge = assets.get_sprite(assets.GAUGE, bar.width, bar.height)
                    # Decouper la jauge evite de comprimer ses pixels a chaque mouvement.
                    visible = pygame.Rect(0, 0, track.left - bar.left + fill_width, bar.height)
                    screen.blit(gauge, bar, visible)
                cursor_width = max(1, round(bar.height * assets.CURSOR.get_width() / assets.CURSOR.get_height()))
                cursor = assets.get_sprite(assets.CURSOR, cursor_width, bar.height)
                handle = cursor.get_rect(center=(track.left + fill_width, bar.centery))
                screen.blit(cursor, handle)
            elif label in self.muted:
                toggle_size = max(1, round(settings.SETTINGS_TOGGLE_SIZE * scale))
                toggle_rect = pygame.Rect(rect.left + 3 * padding, 0, toggle_size, toggle_size)
                toggle_rect.centery = rect.centery
                toggle_sprite = assets.BUTTON_ON if selected else assets.BUTTON_OFF
                toggle_rect = self.get_pixel_rect(toggle_sprite, toggle_rect)
                screen.blit(assets.get_sprite(toggle_sprite, toggle_rect.width, toggle_rect.height), toggle_rect)
                lines = label.split(" ", 1)
                for index, line in enumerate(lines):
                    surface = font.render(line, True, text_color)
                    screen.blit(surface, surface.get_rect(midleft=(
                        toggle_rect.right + padding,
                        rect.centery + (index - 0.5) * font.get_height(),
                    )))
            else:
                text = label.replace("SELECT ", "SELECT\n")
                draw_button(screen, rect, text, sprite, font, text_color)


def draw_quit_button(screen, width, height, marge):
    dw, dh = get_scale(width, height)
    # La meme echelle conserve les proportions du rectangle.
    button_scale = min(dw, dh)
    button_width = max(1, int(settings.DEFAULT_QUIT_BUTTON_WIDTH * button_scale))
    button_height = max(1, int(settings.DEFAULT_QUIT_BUTTON_HEIGHT * button_scale))
    settings_width = max(1, int(settings.DEFAULT_SETTINGS_BUTTON_WIDTH * button_scale))
    settings_x = width - int(settings.DEFAULT_SETTINGS_BUTTON_MARGE * dw) - settings_width
    # Le centre est le miroir de SETTINGS, quelle que soit la largeur de QUIT GAME.
    settings_center_x = settings_x + settings_width // 2
    menu_bottom = get_main_menu_bottom(height, dh, marge)
    rect = game.create_rect(0, menu_bottom - button_height, button_width, button_height)
    rect.centerx = width - settings_center_x

    if rect.collidepoint(pygame.mouse.get_pos()):
        sprite = assets.BUTTON_HOVER
        text_color = settings.TEXT_HOVER_COLOR
        font = assets.create_hover_font(settings.DEFAULT_QUIT_FONT, button_scale)
        rect = rect.inflate(settings.QUIT_HOVER_GROWTH, settings.QUIT_HOVER_GROWTH)
        rect.bottom = menu_bottom
    else:
        sprite = assets.BUTTON
        text_color = settings.BUTTON_COLOR
        font = assets.create_font(settings.DEFAULT_QUIT_FONT, button_scale)

    draw_button(screen, rect, "QUIT GAME", sprite, font, text_color)
    return rect


def draw_game_over(screen, width, height, options):
    
    mouse_pos = pygame.mouse.get_pos()
    
    buttons = deque([])
    
    dw, dh = get_scale(width, height)
    
    button_width = max(settings.DEFAULT_BUTTON3_MIN_WIDTH, int(settings.DEFAULT_BUTTON3_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON3_MIN_HEIGHT, int(settings.DEFAULT_BUTTON3_HEIGHT * dh))
    button_offset = max(settings.DEFAULT_BUTTON3_MIN_MARGE, int(settings.DEFAULT_BUTTON3_MARGE * dh))
    
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
            text_color = settings.BUTTON_COLOR
            font = menu_font
            
        buttons.append((button_text, button_rect))
        
        draw_button(screen, button_rect, button_text, sprite, font, text_color)
        
        x += button_pos
        
    return buttons

def print_game_result(screen, game_result, width, height):
    
    dw, dh = get_scale(width, height)
    
    mid_w = width // 2
    
    score_width = max(settings.DEFAULT_RESULT_MIN_WIDTH, int(settings.DEFAULT_RESULT_WIDTH * dw))
    score_height = max(settings.DEFAULT_RESULT_MIN_HEIGHT, int(settings.DEFAULT_RESULT_HEIGHT * dh))
    
    x = mid_w - (score_width // 2)
    y = int(50 * dh)
    
    sprite = assets.BANNER_SCREEN
    
    rect = game.create_rect(x, y, score_width, score_height)
    font = assets.create_font(settings.DEFAULT_TITLE_FONT, dh)
    
    draw_button(screen, rect, game_result, sprite, font, settings.TITLE_COLOR)
    
def second_menu_setup(states, width, height, marge):
    
    mouse_pos = pygame.mouse.get_pos()
    
    states_len = len(states)
    
    dw, dh = get_scale(width, height)
    
    button_width = max(settings.DEFAULT_BUTTON2_MIN_WIDTH, int(settings.DEFAULT_BUTTON2_WIDTH * dw))
    button_height = max(settings.DEFAULT_BUTTON2_MIN_HEIGHT, int(settings.DEFAULT_BUTTON2_HEIGHT * dh))
    
    menu_height = max(settings.DEFAULT_BUTTON_MIN_HEIGHT, int(settings.DEFAULT_BUTTON_HEIGHT * dh))
    menu_offset = max(settings.DEFAULT_BUTTON_MIN_MARGE, int(settings.DEFAULT_BUTTON_MARGE * dh))
    
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
        text_color = settings.TEXT_HOVER_COLOR if mode else settings.BUTTON_COLOR
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
        return_text_color = settings.BUTTON_COLOR
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

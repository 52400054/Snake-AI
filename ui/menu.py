# ==========================================
# IMPORTS
# ==========================================
import pygame
import os
from core.config import WINDOW_HEIGHT, WINDOW_WIDTH, GRID_SIZE, GRASS_COLOR_1, GRASS_COLOR_2

# ==========================================
# CLASSES
# ==========================================
class Menu:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        
        self.title_font = pygame.font.SysFont('comicsansms', 80, bold=True)
        self.font = pygame.font.SysFont('comicsansms', 40, bold=True)

        self.options = [
            "1. Play Manual",
            "2. AI (A* Algorithm)",
            "3. AI (Q-Learning)",
            "4. Quit"
        ]
        
        self.selected_index = 0

        apple_path = os.path.join('assets', 'images', 'apple.png')
        if os.path.exists(apple_path):
            self.cursor_img = pygame.transform.scale(pygame.image.load(apple_path).convert_alpha(), (40, 40))
        else:
            self.cursor_img = None
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_index
        return None
    
    def draw_background(self):
        for row in range(WINDOW_HEIGHT // GRID_SIZE):
            for col in range(WINDOW_WIDTH // GRID_SIZE):
                color = GRASS_COLOR_1 if (row + col) % 2 == 0 else GRASS_COLOR_2
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw(self):
        self.draw_background()

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130)) 
        self.screen.blit(overlay, (0, 0))
        
        title_text = "Snake Game AI"
        shadow_surf = self.title_font.render(title_text, True, (30, 30, 30))
        title_surf = self.title_font.render(title_text, True, (255, 255, 255))
        
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        shadow_rect = shadow_surf.get_rect(center=(WINDOW_WIDTH // 2 + 5, WINDOW_HEIGHT // 4 + 5))

        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, title_rect)

        start_y = WINDOW_HEIGHT // 2 - 20
        for i, option in enumerate(self.options):
            color = (255, 215, 0) if i == self.selected_index else (200, 200, 200)
            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * 65))
            
            shadow_text = self.font.render(option, True, (0, 0, 0))
            self.screen.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
            
            self.screen.blit(text_surf, text_rect)

            if i == self.selected_index and self.cursor_img is not None:
                cursor_x = text_rect.left - 50
                cursor_y = text_rect.centery - 20
                self.screen.blit(self.cursor_img, (cursor_x, cursor_y))

        pygame.display.flip()
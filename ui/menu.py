import pygame
from core.config import WINDOW_HEIGHT, WINDOW_WIDTH, BG_COLOR

class Menu:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 48)

        self.options = [
            "1. Play Manual",
            "2. AI (A* Algorithm)",
            "3. AI (Q-Learning)",
            "4. Quit"
        ]
        
        self.selected_index = 0
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_index
        return None
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
        title_surf = self.title_font.render("Snake AI", True, (100, 255, 100))
        title_rect = title_surf.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        self.screen.blit(title_surf, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 60))
            self.screen.blit(text_surf, text_rect)
        pygame.display.flip()        
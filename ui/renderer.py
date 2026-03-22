import pygame
from core.config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, BG_COLOR, GRID_COLOR

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        
    def lerp(self, a, b, alpha):
        return a + (b - a) * alpha
    
    def draw_grid(self):
        self.screen.fill(BG_COLOR)
        
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
            
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
            
    def draw_food(self, food):
        
        food_rect = pygame.Rect(
            food.position[0] * GRID_SIZE,
            food.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )        
        pygame.draw.rect(self.screen, (255, 50, 50), food_rect, border_radius=10)
    
    def draw_snake(self, snake, alpha):
        if snake.dead:
            alpha = 1.0
            
        for i, segment in enumerate(snake.body):
            if i < len(snake.old_body):
                old_segment = snake.old_body[i]
            else:
                old_segment = segment
                
            render_x = self.lerp(old_segment[0], segment[0], alpha) * GRID_SIZE
            render_y = self.lerp(old_segment[1], segment[1], alpha) * GRID_SIZE

            seg_rect = pygame.Rect(render_x, render_y, GRID_SIZE, GRID_SIZE)
            
            if i == 0:
                pygame.draw.rect(self.screen, (100, 255, 100), seg_rect, border_radius=8)
            else:
                pygame.draw.rect(self.screen, (50, 255, 50), seg_rect, border_radius=6)
                
    def render_frame(self, snake, food, alpha):
        
        self.draw_grid()
        self.draw_food(food)
        self.draw_snake(snake, alpha)

        if snake.dead:
            font = pygame.font.SysFont(None, 64)
            text = font.render("Game Over - Press R to return to Menu", True, (255, 50, 50))
            text_rect = text.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

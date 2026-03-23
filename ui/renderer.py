# ==========================================
# IMPORTS
# ==========================================
import pygame, os
from core.config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, BG_COLOR, GRID_COLOR, GRASS_COLOR_1, GRASS_COLOR_2

# ==========================================
# CLASSES
# ==========================================
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        
        self.images = {}
        img_dir = os.path.join('assets', 'images')

        for img_name in os.listdir(img_dir):
            if img_name.endswith('.png'):
                key = img_name.split('.')[0]
                img = pygame.image.load(os.path.join(img_dir, img_name)).convert_alpha()
                self.images[key] = pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE))
        
    def lerp(self, a, b, alpha):
        return a + (b - a) * alpha
    
    def draw_grid(self):
        for row in range(WINDOW_HEIGHT // GRID_SIZE):
            for col in range(WINDOW_WIDTH // GRID_SIZE):
                if (row + col) % 2 == 0:
                    color = GRASS_COLOR_1
                else:
                    color = GRASS_COLOR_2
                    
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, color, rect)
            
    def draw_food(self, food):
        render_x = food.position[0] * GRID_SIZE
        render_y = food.position[1] * GRID_SIZE
        self.screen.blit(self.images['apple'], (render_x, render_y))
    
    def draw_snake(self, snake, alpha):
        if snake.dead:
            alpha = 1.0

        p = [snake.body[0]] + snake.old_body

        def get_direction(current, neighbor):
            return current[0] - neighbor[0], current[1] - neighbor[1]

        shapes = []
        for i in range(len(p)):
            if i == 0:
                if snake.direction == (0, -1):   img = self.images['head_up']
                elif snake.direction == (0, 1):  img = self.images['head_down']
                elif snake.direction == (-1, 0): img = self.images['head_left']
                elif snake.direction == (1, 0):  img = self.images['head_right']
            
            elif i == len(p) - 1:
                dx, dy = get_direction(p[i-1], p[i])
                if dx == 1:   img = self.images['tail_left']
                elif dx == -1:img = self.images['tail_right']
                elif dy == 1: img = self.images['tail_up']
                else:         img = self.images['tail_down']
            
            else:
                dx_prev, dy_prev = get_direction(p[i-1], p[i])
                dx_next, dy_next = get_direction(p[i+1], p[i])

                if dy_prev == 0 and dy_next == 0:
                    img = self.images['body_horizontal']
                elif dx_prev == 0 and dx_next == 0:
                    img = self.images['body_vertical']
                else:
                    if (dx_prev == -1 and dy_next == -1) or (dx_next == -1 and dy_prev == -1):
                        img = self.images['body_topleft']
                    elif (dx_prev == -1 and dy_next == 1) or (dx_next == -1 and dy_prev == 1):
                        img = self.images['body_bottomleft']
                    elif (dx_prev == 1 and dy_next == -1) or (dx_next == 1 and dy_prev == -1):
                        img = self.images['body_topright']
                    elif (dx_prev == 1 and dy_next == 1) or (dx_next == 1 and dy_prev == 1):
                        img = self.images['body_bottomright']
                    else:
                        img = self.images['body_horizontal']
            shapes.append(img)

        for i in range(1, len(p) - 1):
            render_x = p[i][0] * GRID_SIZE
            render_y = p[i][1] * GRID_SIZE
            self.screen.blit(shapes[i], (render_x, render_y))

        tail_x = self.lerp(p[-1][0], p[-2][0], alpha) * GRID_SIZE
        tail_y = self.lerp(p[-1][1], p[-2][1], alpha) * GRID_SIZE
        self.screen.blit(shapes[-1], (tail_x, tail_y))

        head_x = self.lerp(p[1][0], p[0][0], alpha) * GRID_SIZE
        head_y = self.lerp(p[1][1], p[0][1], alpha) * GRID_SIZE
        self.screen.blit(shapes[0], (head_x, head_y))
                
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

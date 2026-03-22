# ==========================================
# IMPORTS
# ==========================================
import sys, pygame
from core.config import *
from core.snake import *
from core.food import *
from ui.renderer import *
from ui.menu import *
from ai.classical.a_star import AStarAI
from ai.ml.agent import Agent

# ==========================================
# MAIN GAME LOOP
# ==========================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake AI")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    renderer = Renderer(screen)
    menu = Menu(screen)

    astar_ai = AStarAI()
    ml_agent = Agent()
    
    record = 0
    score = 0
    frame_iteration = 0

    running = True
    accumulator = 0.0
    
    game_state = "MENU"
    current_mode = None
    
    while running:
        
        dt = clock.tick(FPS) / 1000.0
        accumulator += dt
        
        # ==========================================
        # 1. EVENT HANDLING
        # ==========================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == "MENU":
                selected = menu.handle_input(event)
                if selected == 0:
                    game_state = "PLAYING"
                    current_mode = "MANUAL"
                    snake = Snake()
                    food = Food()
                elif selected == 1:
                    game_state = "PLAYING"
                    current_mode = "ASTAR"
                    snake = Snake()
                    food = Food()
                elif selected == 2:
                    game_state = "PLAYING"
                    current_mode = "ML"
                    snake, food, score, frame_iteration = Snake(), Food(), 0, 0
                elif selected == 3:
                    running = False
            elif game_state == "PLAYING" or game_state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if game_state == "GAME_OVER" and event.key == pygame.K_r:
                        game_state = "MENU"
                    elif game_state == "PLAYING" and current_mode == "MANUAL":
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            snake.change_direction(UP)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            snake.change_direction(DOWN)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            snake.change_direction(LEFT)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            snake.change_direction(RIGHT)
        # CHẾ ĐỘ THỬ VÀ SAI
        # tick_rate_to_use = TIME_PER_TICK if current_mode != "ML" else (TIME_PER_TICK / 100)
        # CHẾ ĐỘ BÌNH THƯỜNG
        tick_rate_to_use = TIME_PER_TICK
        
        # ==========================================
        # 2. LOGIC UPDATE (FIXED TIMESTEP)
        # ==========================================
        if accumulator > 0.1:
            accumulator = 0.1
        while accumulator >= tick_rate_to_use:
            if current_mode == "ML":
                pygame.event.pump()
            if game_state == "PLAYING":
                reward = 0
                
                state_old = []
                final_move = []

                if current_mode == "ASTAR":
                    next_dir = astar_ai.get_next_direction(snake, food)
                    if next_dir is not None:
                        snake.change_direction(next_dir)
                elif current_mode == "ML":
                    state_old = ml_agent.get_state(snake, food)
                    final_move = ml_agent.get_action(state_old)
                    next_dir = ml_agent.action_to_direction(final_move, snake.direction)
                    snake.change_direction(next_dir)

                snake.update()
                frame_iteration += 1

                old_dist = abs(snake.body[0][0] - food.position[0]) + abs(snake.body[0][1] - food.position[1])
                
                new_dist = abs(snake.body[0][0] - food.position[0]) + abs(snake.body[0][1] - food.position[1])

                if next_dir is not None: 
                    if new_dist < old_dist:
                        reward = 1
                    else:
                        reward = -1

                if snake.dead or (current_mode == "ML" and frame_iteration > 100 * len(snake.body)):
                    snake.dead = True
                    reward = -10
                    if current_mode != "ML":
                        game_state = "GAME_OVER"
                    else:
                        state_new = ml_agent.get_state(snake, food)
                        ml_agent.train_short_memory(state_old, final_move, reward, state_new, True)
                        ml_agent.remember(state_old, final_move, reward, state_new, True)
                        
                        ml_agent.n_games += 1
                        ml_agent.train_long_memory()
                        if score > record:
                            record = score
                            ml_agent.model.save("best_model.pth")

                        print(f"Game: {ml_agent.n_games} | Score: {score} | Record: {record}")

                        snake, food, score, frame_iteration = Snake(), Food(), 0, 0
                        continue

                if not snake.dead:
                    if snake.body[0] == food.position:
                        snake.grow()
                        food.respawn(snake.body)
                        score += 1
                        reward = 10
                        frame_iteration = 0
                        
                    if current_mode == "ML":
                        state_new = ml_agent.get_state(snake, food)
                        ml_agent.train_short_memory(state_old, final_move, reward, state_new, False)
                        ml_agent.remember(state_old, final_move, reward, state_new, False)
            
            accumulator -= tick_rate_to_use
        
        # ==========================================
        # 3. GRAPHICS RENDERING (INTERPOLATION)
        # ==========================================
        if game_state == "MENU":
            menu.draw()
        else:
            if current_mode == "ML" and snake.dead:
                alpha = 1.0
            else:
                alpha = accumulator / TIME_PER_TICK
            renderer.render_frame(snake, food, alpha)

            title = f"Snake AI | "
            if current_mode == "ML":
                title += f"Game: {ml_agent.n_games} - Score: {score} - Record: {record}"
            else:
                title += f"FPS: {int(clock.get_fps())} | Mode: {current_mode}"
            pygame.display.set_caption(title)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
import torch
import random
import numpy as np
from collections import deque
from core.config import WINDOW_HEIGHT, WINDOW_WIDTH, GRID_SIZE
from core.snake import UP, DOWN, LEFT, RIGHT
from ai.ml.model import LinearQNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = LinearQNet(11, 256, 3)

        import os
        model_path = './ai/ml/best_model.pth'
        if os.path.exists(model_path):
            print("Đã tải thành công bộ não AI (best_model.pth)!")
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval() # Bật chế độ suy luận ròng (không train)

        self.trainer = QTrainer(self.model, lr = LR, gamma=self.gamma)

        self.max_x = (WINDOW_WIDTH // GRID_SIZE) - 1
        self.max_y = (WINDOW_HEIGHT // GRID_SIZE) - 1
        
    def get_state(self, snake, food):
        head = snake.body[0]
        
        point_l = (head[0] - 1, head[1])
        point_r = (head[0] + 1, head[1])
        point_u = (head[0], head[1] - 1)
        point_d = (head[0], head[1] + 1)

        dir_l = snake.direction == LEFT
        dir_r = snake.direction == RIGHT
        dir_u = snake.direction == UP
        dir_d = snake.direction == DOWN

        state = [
            (dir_r and self.is_collision(point_r, snake)) or 
            (dir_l and self.is_collision(point_l, snake)) or 
            (dir_u and self.is_collision(point_u, snake)) or 
            (dir_d and self.is_collision(point_d, snake)),

            (dir_u and self.is_collision(point_r, snake)) or 
            (dir_d and self.is_collision(point_l, snake)) or 
            (dir_l and self.is_collision(point_u, snake)) or 
            (dir_r and self.is_collision(point_d, snake)),

            (dir_d and self.is_collision(point_r, snake)) or 
            (dir_u and self.is_collision(point_l, snake)) or 
            (dir_r and self.is_collision(point_u, snake)) or 
            (dir_l and self.is_collision(point_d, snake)),
            
            dir_l, dir_r, dir_u, dir_d,
            
            food.position[0] < head[0],  
            food.position[0] > head[0],  
            food.position[1] < head[1],  
            food.position[1] > head[1]   
        ]
        
        return np.array(state, dtype=int)

    def is_collision(self, pt, snake):
        if pt[0] < 0 or pt[0] > self.max_x or pt[1] < 0 or pt[1] > self.max_y:
            return True
        if pt in set(snake.body[:-1]):
            return True
        return False
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
            
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # self.epsilon = 80 - self.n_games # Chế độ thử và sai
        self.epsilon = 0 # Chế độ đi khôn
        final_move = [0,0,0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
        
    
    def action_to_direction(self, action, current_direction):
        clock_wise = [UP, RIGHT, DOWN, LEFT]
        idx = clock_wise.index(current_direction)

        if np.array_equal(action, [1, 0, 0]):
            return clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            return clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            return clock_wise[next_idx]
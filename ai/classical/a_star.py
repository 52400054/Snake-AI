# ==========================================
# IMPORTS
# ==========================================
import heapq
from core.config import WINDOW_HEIGHT, WINDOW_WIDTH, GRID_SIZE
from core.snake import UP, DOWN, LEFT, RIGHT

# ==========================================
# CLASSES
# ==========================================
class Node:
    def __init__(self, position, parent = None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

class AStarAI:
    def __init__(self):
        self.max_x = (WINDOW_WIDTH // GRID_SIZE) - 1
        self.max_y = (WINDOW_HEIGHT // GRID_SIZE) - 1

    def get_next_direction(self, snake, food):
        start = snake.body[0]
        target = food.position

        open_list = []
        closed_set = set()

        start_node = Node(start)
        heapq.heappush(open_list, start_node)

        obstacles = set(snake.body[:-1])

        while open_list:
            current_node = heapq.heappop(open_list)
            current_pos = current_node.position

            if current_pos in closed_set:
                continue

            # ĐÃ TÌM THẤY MỒI
            if current_pos == target:
                path = []
                while current_node is not None:
                    path.append(current_node.position)
                    current_node = current_node.parent

                if len(path) > 1:
                    next_pos = path[-2]
                    return self._get_direction(start, next_pos)
                else:
                    return self._survival_mode(snake)

            closed_set.add(current_pos)

            for direction in [UP, DOWN, LEFT, RIGHT]:
                node_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                                                                       
                if node_pos[0] < 0 or node_pos[0] > self.max_x or node_pos[1] < 0 or node_pos[1] > self.max_y:                                                                      
                    continue

                if node_pos in obstacles:
                    continue

                if node_pos in closed_set:
                    continue

                child = Node(node_pos, current_node)
                child.g = current_node.g + 1
                child.h = abs(node_pos[0] - target[0]) + abs(node_pos[1] - target[1])                                                                                           
                child.f = child.g + child.h

                heapq.heappush(open_list, child)

        return self._survival_mode(snake)

    def _get_direction(self, current, next_pos):
        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]

        if dx > 0: dx = 1
        elif dx < 0: dx = -1
        
        if dy > 0: dy = 1
        elif dy < 0: dy = -1

        return (dx, dy)
        
    def _survival_mode(self, snake):
        start = snake.body[0]
        obstacles = set(snake.body[:-1])

        safe_moves = []

        for direction in [UP, DOWN, LEFT, RIGHT]:
            if (direction[0] * -1, direction[1] * -1) == snake.direction:       
                continue
                
            node_pos = (start[0] + direction[0], start[1] + direction[1])       
            if 0 <= node_pos[0] <= self.max_x and 0 <= node_pos[1] <= self.max_y:                                                                                               
                if node_pos not in obstacles:
                    safe_moves.append(direction)
                    
        if safe_moves:
            if snake.direction in safe_moves:
                return snake.direction
            return safe_moves[0]
            
        return snake.direction
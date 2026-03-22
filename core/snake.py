from core.config import WINDOW_HEIGHT, WINDOW_WIDTH, GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        start_x = (WINDOW_WIDTH // GRID_SIZE) // 2
        start_y = (WINDOW_HEIGHT // GRID_SIZE) // 2

        self.body = [(start_x, start_y), (start_x, start_y + 1), (start_x, start_y + 2)]

        self.old_body = list(self.body)

        self.direction = UP
        self.next_direction = UP
        self.grow_pending = False
        self.dead = False
        
    def update(self):
        if self.dead:
            return
        
        self.direction = self.next_direction
        
        self.old_body = list(self.body)

        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        max_x = (WINDOW_WIDTH // GRID_SIZE) - 1
        max_y = (WINDOW_HEIGHT // GRID_SIZE) - 1

        if new_head[0] < 0 or new_head[0] > max_x or new_head[1] < 0 or new_head[1] > max_y or new_head in self.body[:-1]:
            self.dead = True
            return

        self.body.insert(0, new_head)

        if self.grow_pending:
            self.grow_pending = False
        else: 
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.next_direction = new_dir
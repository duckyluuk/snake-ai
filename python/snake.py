import random
import time
import pygame

class GameBoard:
    def __init__(self, size=10, block_size=10):
        self.size = size
        self.block_size = block_size
        self.snake = Snake(size)
        self.fruit = Fruit(size, self.snake)
        self.alive = True
        self.frame_time = 0
        self.delay_time = 0.01
        self.last_time = False
        self.screen = pygame.display.set_mode((size * 10, size * 10))
        self.snakePath = []
        
    def game_loop(self):
        if not self.last_time:
            self.last_time = time.time()
        while self.alive:
            self.frame_time += time.time() - self.last_time
            self.last_time = time.time()
            if self.frame_time > self.delay_time:
                self.render()
                self.frame_time %= self.delay_time
                if True:
                    if self.snakePath == []:
                        self.snakePath = self.dijkstra()
                    
                    if self.snakePath != None:
                        self.snake.set_direction(self.snakePath.pop(0))
                    
                self.alive = self.snake.move(self.fruit)
                
        print(len(self.snake.blocks))
            
    def render(self):
        self.screen.fill((0, 0, 0))
        for block in self.snake.blocks:
            pygame.draw.rect(self.screen, (255, 255, 255), (block[0] * self.block_size, block[1] * self.block_size, self.block_size, self.block_size))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.fruit.x * self.block_size, self.fruit.y * self.block_size, self.block_size, self.block_size))
        pygame.display.flip()
        
    def dijkstra(self):
        import heapq
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for index, block in enumerate(self.snake.blocks):
            grid[block[0]][block[1]] = index + 2
        # each node in the queue consists of [block, path, moves]
        queue = [(self.get_dis(*self.snake.blocks[-1]), self.snake.blocks[-1], [], [])]
        while queue:
            node = heapq.heappop(queue)
            for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x = node[1][0] + dir[0]
                y = node[1][1] + dir[1]
                if (x, y) in node[2]:
                    continue

                travelled = len(node[2]) + 1
                path = node[2] + [(x, y)]
                directions = node[3] + [dir]
                if x < 0 or x >= self.size or y < 0 or y >= self.size:
                    continue
                if grid[x][y] > travelled or grid[x][y] < 0:
                    continue
                if (x, y) == (self.fruit.x, self.fruit.y):
                    return directions
                grid[x][y] = -1
                heapq.heappush(queue, (self.get_dis(x, y), (x, y), path, directions))
                
        return None
    
    def get_dis(self, x, y):
        return abs(x - self.fruit.x) + abs(y - self.fruit.y)


class Snake:
    def __init__(self, size):
        self.size = size
        self.blocks = [(size // 2 - 2, size // 2), (size // 2 - 1, size // 2), (size // 2, size // 2)]
        self.direction = (1, 0)
        
    def move(self, fruit):
        head = self.blocks[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        if new_head[0] < 0 or new_head[0] >= self.size or new_head[1] < 0 or new_head[1] >= self.size:
            return False
        if new_head in self.blocks:
            return False
        self.blocks.append(new_head)
        if new_head == (fruit.x, fruit.y):
            fruit.move(self)
        else:
            self.blocks.pop(0)
        return True
    
    def set_direction(self, direction):
        self.direction = direction
        
        
        
        
class Fruit:
    def __init__(self, size, snake):
        self.size = size
        self.move(snake)
        
    def move(self, snake):
        positions = [(x,y) for x in range(self.size) for y in range(self.size)]
        positions = list(set(positions) - set(snake.blocks))
        
        position = random.choice(positions)
        self.x = position[0]
        self.y = position[1]
        
        
if __name__ == "__main__":
    pygame.init()
    game = GameBoard(20, 10)
    game.game_loop()
    time.sleep(5)
    pygame.quit()
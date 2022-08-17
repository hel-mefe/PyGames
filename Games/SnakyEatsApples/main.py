from tkinter.tix import CELL
import pygame, sys, random
from pygame.math import Vector2

CELL_SIZE = 40
CELL_NUMBER = 20

class Fruit:
    def __init__(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x) * CELL_SIZE, int(self.pos.y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)
    
    def move_snake(self):
        if (self.new_block):
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def randomize(self):
        self.fruit.x = random.randint(0, CELL_NUMBER - 1)
        self.fruit.y = random.randint(0, CELL_NUMBER - 1)
        self.fruit.pos = Vector2(self.fruit.x, self.fruit.y)

    def check_collision(self):
        if (self.fruit.pos == self.snake.body[0]):
            self.randomize()
            self.snake.add_block()

WIDTH = CELL_SIZE * CELL_NUMBER
HEIGHT = WIDTH
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
running = True
test_surface = pygame.Surface((100, 200))

game = Main()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            pygame.quit()
            sys.exit()
        if (event.type == SCREEN_UPDATE):
            game.update()
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_UP and game.snake.direction.y != 1):
                game.snake.direction = Vector2(0, -1)
            if (event.key == pygame.K_DOWN and game.snake.direction.y != -1):
                game.snake.direction = Vector2(0, 1)
            if (event.key == pygame.K_RIGHT and game.snake.direction.x != -1):
                game.snake.direction = Vector2(1, 0)
            if (event.key == pygame.K_LEFT and game.snake.direction.x != 1):
                game.snake.direction = Vector2(-1, 0)
    screen.fill((175, 215, 70))
    game.draw_elements()
    pygame.display.update()

import pygame
import os

def get_path():
    file_path = __file__.split('/')
    path = ''
    for i in range (len(file_path) - 1):
        path += '/'
        path += file_path[i]
    return (path)


# Game initializer
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('PingPong Game')

# Macros
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 700, 500
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont('comicsans', 50)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_MUSIC = pygame.mixer.music.load(get_path() + '/backgroundMusic.mp3')

# Game classes
class Paddle:
    COLOR = WHITE
    VEL = 7

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if (up):
            self.y -= self.VEL
        else:
            self.y += self.VEL

class Ball:
    MAX_VEL = 5
    COLOR = (255, 100, 100)

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

# Game functionalities
def draw(win, paddles, ball, scores):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{scores[0]}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{scores[1]}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)

    j = 0
    for i in range(0, HEIGHT, HEIGHT//20):
        m = HEIGHT / HEIGHT // 20
        # if not(j % 2):
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 2, i, 2, HEIGHT//20))
        pygame.draw.circle(win, WHITE, (WIDTH//2, HEIGHT//2), 6)
        if (j >= m):
            pygame.draw.circle(win, WHITE, (WIDTH // 2, HEIGHT // 2), 110, 2)
        j += 1
    
    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if (ball.y + ball.radius >= HEIGHT):
        ball.y_vel *= -1
    elif (ball.y - ball.radius <= 0):
        ball.y_vel *= -1
    
    if (ball.x_vel < 0):
        if (ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height):
            if (ball.x - ball.radius <= left_paddle.x + left_paddle.width):
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel 
    else:
        if (ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height):
            if (ball.x + ball.radius >= right_paddle.x):
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel 


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if (keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0):
        left_paddle.move(up=True)
    if (keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT):
        left_paddle.move(up=False)
    if (keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0):
        right_paddle.move(up=True)
    if (keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT):
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_score, left_score = 0, 0
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    while (run):
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, [left_score, right_score])
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
                break 
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        if (ball.x <= 0):
            right_score += 1
            ball.x = WIDTH // 2 - ball.radius
            ball.y = HEIGHT // 2 - ball.radius
            ball.x_vel = -5
            ball.y_vel = 0
        elif (ball.x >= WIDTH):
            left_score += 1
            ball.x = WIDTH // 2 - ball.radius
            ball.y = HEIGHT // 2 - ball.radius
            ball.x_vel = 5
            ball.y_vel = 0
    pygame.quit()

if (__name__ == '__main__'):
    main()
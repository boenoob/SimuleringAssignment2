import pygame
import math
#from pygame.sndarray import array


WIDTH, HEIGHT = 900, 500
RADIUS = 45

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

balls = []
priorityQueue = []

FPS = 60


# Ball object
class Ball:
    def __init__(self, position, radius, velocity):
        self.radius = radius
        self.velocity = velocity
        self.position = position
        self.color = BLUE


def draw_window():
    WIN.fill(WHITE)
    # draw balls
    for ball in balls:
        pos = pygame.Vector2(ball.position.x, ball.position.y)
        pygame.draw.circle(WIN, ball.color, pos, ball.radius)
    pygame.display.update()


def init():
    # append to balls array
    number_of_balls = 1
    for i in range(number_of_balls):
        pos = pygame.Vector2((RADIUS+1+i*100), (RADIUS+1))
        vel = pygame.Vector2((1), (-2))
        balls.append(Ball(pos, RADIUS, vel))


def updatePos():
    # loop all balls
    for i in range(len(balls)):
        # update ball position based on velocity
        balls[i].position.x += balls[i].velocity.x
        balls[i].position.y += balls[i].velocity.y


# Check when balls will collide based on timesteps


def BallCollsion(balls):
    for i in range(len(balls)):
        for j in range(1000):
            if (balls[i].position.x == RADIUS or balls[i].position.x == (WIDTH-RADIUS)) and (balls[i].position.y == RADIUS or balls[i].position.y == (WIDTH-RADIUS)):
                print("Crash with a wall at ")
                print(balls[i].position)
            balls[i].position.x += balls[i].velocity.x
            balls[i].position.y += balls[i].velocity.y


def main():
    clock = pygame.time.Clock()
    run = True
    init()
    BallCollsion(balls)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        updatePos()
        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()

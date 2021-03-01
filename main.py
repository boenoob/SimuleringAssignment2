import pygame
import math
from pygame.sndarray import array


WIDTH, HEIGHT = 900, 500
RADIUS = 45

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
balls = []

FPS = 60


#Ball object
class Ball:
    def __init__(self, position, radius, velocity):
        self.radius = radius
        self.velocity = velocity
        self.position = position
        self.color = RED
        self.collisions = []


def draw_window():
    WIN.fill(WHITE)
    #draw balls
    for ball in balls:
        pos = pygame.Vector2(ball.position.x, ball.position.y)
        pygame.draw.circle(WIN, ball.color, pos, ball.radius)
    pygame.display.update()

def init():
    #append to balls array
    number_of_balls = 6
    for i in range(number_of_balls):
        pos = pygame.Vector2()
        vel = pygame.Vector2()
        vel.x = -1 + i * (-1)
        vel.y = -2 + i * (-1)
        pos.x = 50 + i * 3
        pos.y = 50 + i * 4
        balls.append(Ball(pos, RADIUS, vel))

def update():

    #loop all balls
    for i in range(len(balls)):

        #Is ball colliding?
        if len(balls[i].collisions) > 0:
            balls[i].color = GREEN
        else:
            balls[i].color = RED

        #ball collision
        for j in range(len(balls)):
            if i != j: #not collide with self
                ball1 = balls[i]
                ball2 = balls[j]
                if BallCollsion(ball1, ball2):
                    if not (ball2 in ball1.collisions):
                        ball1.collisions.append(ball2)
                        ball2.collisions.append(ball1)

                else:
                    if ball2 in ball1.collisions:
                        ball1.collisions.remove(ball2)
                        ball2.collisions.remove(ball1)

        #edge collision
        if balls[i].position.x - balls[i].radius < 0 or balls[i].position.x + balls[i].radius > WIDTH:
            balls[i].velocity.x = -balls[i].velocity.x
        if balls[i].position.y - balls[i].radius < 0 or balls[i].position.y + balls[i].radius > HEIGHT:
            balls[i].velocity.y = -balls[i].velocity.y
        
        #update ball velocity based on collisions / redirection                   FIX DET HER!

    

        #update ball position based on velocity
        balls[i].position.x += balls[i].velocity.x
        balls[i].position.y += balls[i].velocity.y
        
#Returns vector between balls
def VectorBetweenBalls(ball1, ball2):
    distance = pygame.Vector2()
    distance.x = ball1.position.x - ball2.position.x
    distance.y = ball1.position.y - ball2.position.y
    return distance

#Check if 2 balls are colliding
def BallCollsion (ball1, ball2):
    distance = VectorBetweenBalls(ball1, ball2).magnitude()
    radiusSum = ball1.radius + ball2.radius
    if distance < radiusSum:
        return True
    return False

#Ikke brukt (MÅ FIKSES)
#
def BallRecoilVector(ball1, ball2):
    #Vector between walls
    distance = VectorBetweenBalls(ball1, ball2)
    
    #Angle between distance vector
    angleBall1 = math.acos(ball1.velocity.dot(distance) / (ball1.velocity.magnitude * ball1.velocity.magnitude))
    angleBall2 = math.acos(ball2.velocity.dot(distance.reflect_ip()) / (ball2.velocity.magnitude * ball2.velocity.magnitude))

    #Find xy-components
    #ball 1
    ball1.velocity.y = ball1.velocity.magnitude() * math.sin(angleBall1)
    ball1.velocity.x = ball1.velocity.magnitude() * math.cos(angleBall1)

    #ball 2
    ball2.velocity.y = ball2.velocity.magnitude() * math.sin(angleBall2)
    ball2.velocity.x = ball2.velocity.magnitude() * math.cos(angleBall2)

    

# elastic impact (FUNKER, MEN IKKE I BRUK)
def VelocityAfterImpact(ball1Mass, ball1Vel,  ball2Mass, ball2Vel):
    C1 = ball1Mass * ball1Vel + ball2Mass * ball2Vel
    C2 = ball1Mass * ball1Vel**2 + ball2Mass * ball2Vel**2

    A = ball1Mass + (ball1Mass**2)/ball2Mass

    B = -(2 * C1 * ball1Mass/ball2Mass)

    C = C1**2/ball2Mass - C2

    #discriminant
    dis = B**2 - 4 * A * C

    ball1NewVel = 0
    if ball1Vel > 0:
        ball1NewVel = (-B - math.sqrt(dis)) / (2 * A)
    else:
        ball1NewVel = (-B + math.sqrt(dis)) / (2 * A)

    ball2NewVel = (C1 - ball1Mass * ball1NewVel)/ball2Mass

    return pygame.Vector2(ball1NewVel, ball2NewVel)



def main():
    clock = pygame.time.Clock()
    run = True
    init()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False     

        update()
        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
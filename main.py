import pygame

pygame.init()
screen = pygame.display.set_mode((700, 450))
pygame.display.set_caption("PING PONG")
font = pygame.font.SysFont('Ariel', 40)
cpuscore = 0
player = 0
pong = 0
player_y = 80
cpu_y = 80
clock = pygame.time.Clock()
fps = 90
winner = 0
lball = False
levelchange = 0


def txtonscreen(text, font, colour, x, y):
    txt = font.render(text, True, colour)
    screen.blit(txt, (x, y))


class paddles():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 20, 80)
        self.speed = 8

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > 60:
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < 450:
            self.rect.move_ip(0, self.speed)

    def cpumove(self):
        if self.rect.centery < pongball.rect.top and self.rect.bottom < 450:
            self.rect.move_ip(0, self.speed)
        if self.rect.centery > pongball.rect.bottom and self.rect.top > 60:
            self.rect.move_ip(0, -1 * self.speed)

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)


class ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.rect.x + self.rad, self.rect.y + self.rad), self.rad)

    def move(self):
        if self.rect.top < 60:
            self.speed_y *= -1
        if self.rect.bottom > 450:
            self.speed_y *= -1
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 10 or self.rect.right > 690:
            self.winner = -1
        return self.winner

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.rad = 10
        self.rect = pygame.Rect(self.x, self.y, self.rad * 2, self.rad * 2)
        self.speed_x = 1
        self.speed_y = 1
        self.winner = 0


player_paddle = paddles(20, 180)
cpu_paddle = paddles(660, 180)
pongball = ball(200, 200)

run = True
while run:
    screen.fill((0, 0, 0))
    clock.tick(fps)
    player_paddle.draw()
    cpu_paddle.draw()
    if lball == True:
        levelchange += 1
        winner = pongball.move()
        if winner == 0:
            player_paddle.move()
            cpu_paddle.cpumove()
            pongball.draw()
        else:
            lball = False
            if winner == -1:
                cpuscore += 10
            if winner == 1:
                player += 10
    if lball == False:
        if winner == 0:
            txtonscreen('click anywhere to start', font, (255, 255, 255), 190, 125)
        if winner == 1:
            txtonscreen('YOU WIN', font, (255, 255, 255), 280, 150)
            txtonscreen('click anywhere to start', font, (255, 255, 255), 190, 150)
        if winner == -1:
            txtonscreen('YOU LOST', font, (255, 255, 255), 280, 125)
            txtonscreen('click anywhere to start', font, (255, 255, 255), 190, 150)

    txtonscreen('CPU:' + str(cpuscore), font, (255, 0, 0), 580, 30)
    txtonscreen('PLAYER:' + str(player), font, (255, 255, 255), 20, 30)
    txtonscreen('LEVEL  ' + str(abs(pongball.speed_x)), font, (255, 25, 155), 300, 30)
    pygame.draw.line(screen, (255, 255, 255), (0, 60), (700, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_DOWN:
                player_y -= 10
            if event.type == pygame.K_UP:
                player_y += 10
        elif event.type == pygame.MOUSEBUTTONDOWN and lball == False:
            lball = True
            pongball.reset(200, 200)
    if levelchange > 500:
        levelchange = 0
        if pongball.speed_x < 0:
            pongball.speed_x -= 1
        if pongball.speed_x > 0:
            pongball.speed_x += 1
        if pongball.speed_y < 0:
            pongball.speed_y -= 1
        if pongball.speed_y > 0:
            pongball.speed_y += 1
    pygame.display.update()
pygame.quit()

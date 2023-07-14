import pygame
import random

"""
Bugs:
1. Whenever the ball gets stuck in the paddle, bad things happen (also the ball CAN
get stuck in the paddle, which is an issue)
    Bad things: the score goes up really quickly and the ball doesn't move out
2. If the score gets high enough, it will go off screen
"""

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
score = 0
score_increment = 1

# Player class
class Player(pygame.sprite.Sprite):
    # Constructor, draws sprite
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((17, 80))
        self.color = WHITE
        self.surf.fill(self.color)

        self.posy = SCREEN_HEIGHT // 2
        self.posx = SCREEN_WIDTH - (SCREEN_WIDTH//6)
        self.speed = 0.5

        # Determining where the player spawns
        self.rect = self.surf.get_rect(
            center=(
                self.posx, 
                self.posy
            )
        )

    def update(self, pressed_keys):
        # Movement information
        if pressed_keys[K_UP]:
            self.posy = self.posy + (self.speed * -1)
        if pressed_keys[K_DOWN]:
            self.posy = self.posy + (self.speed * 1)

        self.rect = self.surf.get_rect(
        center=(
            self.posx, 
            self.posy
        )
        )

        self.surf.fill(self.color)

        # Making sure we don't go off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def change_rand_color(self):
        self.color = (random.randint(10,255), random.randint(10,255), random.randint(10,255))


# Ball class
class Ball(pygame.sprite.Sprite):
    # Constructor, draws sprite
    def __init__(self):
        super(Ball, self).__init__()
        self.width = 25
        self.height = 25
        self.speed = 0.35
        self.xFac = 1
        self.yFac = -1
        self.posx = SCREEN_WIDTH - (SCREEN_WIDTH - (SCREEN_WIDTH//8))
        self.posy = SCREEN_HEIGHT // 2
        self.color = WHITE

        self.surf = pygame.Surface((self.width, self.height))

        # self.surf, color, width and height, radius
        pygame.draw.circle(self.surf, self.color, (self.width//2, self.height//2), 12)

        # Determining where the ball spawns
        self.rect = self.surf.get_rect(
            center=(
                self.posx, 
                self.posy
            )
        )
    
    def update(self):
        self.posx = self.posx + (self.speed * self.xFac)
        self.posy = self.posy + (self.speed * self.yFac)

        self.rect = self.surf.get_rect(center=(self.posx, self.posy))
        pygame.draw.circle(self.surf, self.color, (self.width//2, self.height//2), 12)

        if (self.posy <= 0) or (self.posy >= SCREEN_HEIGHT):
            self.yFac = self.yFac * -1
        if self.posx <= 0:
            self.xFac = self.xFac * -1

        if self.posx >= SCREEN_WIDTH:
            self.kill()

    def change_rand_color(self):
        self.color = (random.randint(10,255), random.randint(10,255), random.randint(10,255))


    def reset(self):
        self.posx = SCREEN_WIDTH - (SCREEN_WIDTH - (SCREEN_WIDTH//8))
        self.posy = SCREEN_HEIGHT // 2

        self.rect = self.surf.get_rect(
            center=(
                self.posx, 
                self.posy
            )
        )



pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Weird Pong")

# Initializing sprites
player = Player()
ball = Ball()

# Adding sprites into sprite groups
balls = pygame.sprite.Group()
balls.add(ball)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)

running = True

# GAME LOOP
while running:
    # Score printing
    font = pygame.font.Font(None, 36)

    # Processing events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_LEFT:
                ball.reset()

    
    pressed_keys = pygame.key.get_pressed()

    # Updating for movement
    player.update(pressed_keys)
    ball.update()

    # Filling the screen to black
    screen.fill(BLACK)

    # Blitting score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (450,560))
    
    # Blitting all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Bounce back if hit
    if pygame.sprite.spritecollideany(player, balls):
        ball.speed = -ball.speed
        score += score_increment
        ball.change_rand_color()
        player.change_rand_color()

    # Pushing sprites to screen
    pygame.display.flip()

pygame.quit()
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Player class
class Player(pygame.sprite.Sprite):
    # Constructor, draws sprite
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        # Determining where the player spawns
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH - (SCREEN_WIDTH//6), 
                SCREEN_HEIGHT // 2
            )
        )

    def update(self, pressed_keys):
        # Movement information
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        # Making sure we don't go off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Ball class
class Ball(pygame.sprite.Sprite):
    # Constructor, draws sprite
    def __init__(self):
        super(Ball, self).__init__()
        self.width = 25
        self.height = 25
        self.speed = 1

        self.surf = pygame.Surface((self.width, self.height))

        # self.surf, color, width and height, radius
        pygame.draw.circle(self.surf, (255,255,255), (self.width//2, self.height//2), 12)
        # Determining where the ball spawns
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH - (SCREEN_WIDTH - (SCREEN_WIDTH//8)), 
                SCREEN_HEIGHT // 2
            )
        )
    
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left >= SCREEN_WIDTH:
            self.kill()



pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
    # Processing events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    
    pressed_keys = pygame.key.get_pressed()

    # Updating for movement
    player.update(pressed_keys)
    ball.update()

    # Filling the screen to black
    screen.fill((0,0,0))
    
    # Blitting all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Bounce back if hit
    if pygame.sprite.spritecollideany(player, balls):
        ball.speed = -ball.speed

    # Pushing sprites to screen
    pygame.display.flip()

pygame.quit()
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60

background = pygame.image.load("AnimatedStreet.png")
player_img = pygame.image.load("Player.png")
enemy_img = pygame.image.load("Enemy.png")
coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (30, 30))

font = pygame.font.SysFont("Verdana", 20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 40:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 40:
            self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)
        self.speed = 5

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset_position()
        self.value = random.choice([1, 2, 5])

    def reset_position(self):
        self.rect.center = (random.randint(40, WIDTH - 40), -random.randint(100, 300))
        self.value = random.choice([1, 2, 5])

    def move(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > HEIGHT:
            self.reset_position()

player = Player()
enemy = Enemy()
coins = [Coin() for _ in range(3)]

all_sprites = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()

all_sprites.add(player)
all_sprites.add(enemy)
enemies.add(enemy)

for coin in coins:
    all_sprites.add(coin)
    coins_group.add(coin)

coin_score = 0
next_level_threshold = 5

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()
    enemy.move()
    for coin in coins:
        coin.move()

    if pygame.sprite.spritecollideany(player, enemies):
        print("Game Over!")
        pygame.quit()
        break

    collected = pygame.sprite.spritecollide(player, coins_group, False)
    for coin in collected:
        coin_score += coin.value
        coin.reset_position()

        if coin_score % next_level_threshold == 0:
            enemy.speed += 1

    win.blit(background, (0, 0))
    for entity in all_sprites:
        win.blit(entity.image, entity.rect)

    score_text = font.render(f"Coins: {coin_score}", True, BLACK)
    win.blit(score_text, (WIDTH - 140, 10))

    pygame.display.update()

pygame.quit()

import pygame
import random

# ゲーム画面の幅と高さを設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pygameを初期化して、ウィンドウを作成
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ゲーム画面の背景色を設定
background_color = (0, 0, 0)  # (R, G, B)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # プレイヤーの画像を読み込む
        self.image = pygame.image.load("player.png")

        # プレイヤーの位置を設定
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10

    def update(self):
        # キーボードの入力に応じて、プレイヤーを動かす
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # 敵の画像を読み込む
        self.image = pygame.image.load("enemy.png")

        # 敵の位置を設定
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

        # 敵の速度を設定
        self.speedy = random.randrange(1, 8)

    def update(self):
        # 敵を下に動かす
        self.rect.y += self.speedy

        # 敵が画面外に出たら、再び画面内に現れるようにする
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # 弾の画像を読み込む
        self.image = pygame.image.load("bullet.png")

        # 弾の位置を設定
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # 弾の速度を設定
        self.speedy = -10

    def update(self):
        # 弾を上に動かす
        self.rect.y += self.speedy

        # 弾が画面外に出たら、消滅する
        if self.rect.bottom < 0:
            self.kill()


# プレイヤーを作成
player = Player()

# 敵のグループを作成
enemies = pygame.sprite.Group()
for i in range(10):
    enemy = Enemy()
    enemies.add(enemy)

# 弾のグループを作成
bullets = pygame.sprite.Group()

# ゲームループを開始
running = True
while running:
    # ゲーム画面を更新
    screen.fill(background_color)

    # イベントを処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)

    # プレイヤーを更新
    player.update()

    # 敵を更新
    enemies.update()

    # 弾を更新
    bullets.update()

    # 衝突判定
    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, True)
        for hit in hits:
            bullet.kill()

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # 画面に描画
    screen.blit(player.image, player.rect)
    enemies.draw(screen)
    bullets.draw(screen)

    # 画面を更新
    pygame.display.flip()

# Pygameを終了する
pygame.quit()


import pygame

class Enemy:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        
    def damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

# フォントの初期化
pygame.init()
font = pygame.font.Font(None, 24)

# 敵のインスタンスを作成
enemy = Enemy(100, 100, 100)

# メインループ
while True:
    # 画面の更新
    screen.fill((255, 255, 255))
    
    # 敵のHPを表示
    hp_text = font.render(f"Enemy HP: {enemy.hp}", True, (0, 0, 0))
    screen.blit(hp_text, (10, 10))
    
    pygame.display.update()


import pygame
import random

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooting Game")

clock = pygame.time.Clock()

player_img = pygame.image.load("player.png").convert_alpha()
player_x = 300
player_y = 400
player_speed = 5

enemy_img = pygame.image.load("enemy.png").convert_alpha()
enemies = []
enemy_speed = 3
enemy_spawn_delay = 60

bullet_img = pygame.image.load("bullet.png").convert_alpha()
bullets = []
bullet_speed = 10
bullet_delay = 20

explosion_sound = pygame.mixer.Sound("explosion.wav")

def spawn_enemy():
    enemy_x = random.randint(0, screen_width - enemy_img.get_width())
    enemy_y = -enemy_img.get_height()
    enemies.append([enemy_x, enemy_y])

def shoot():
    bullet_x = player_x + player_img.get_width() / 2 - bullet_img.get_width() / 2
    bullet_y = player_y - bullet_img.get_height()
    bullets.append([bullet_x, bullet_y])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed

    if keys[pygame.K_SPACE]:
        if bullet_delay <= 0:
            shoot()
            bullet_delay = 20

    if enemy_spawn_delay <= 0:
        spawn_enemy()
        enemy_spawn_delay = 60

    screen.fill((0, 0, 0))

    for enemy in enemies:
        enemy[1] += enemy_speed
        screen.blit(enemy_img, (enemy[0], enemy[1]))

        if enemy[1] > screen_height:
            enemies.remove(enemy)

    for bullet in bullets:
        bullet[1] -= bullet_speed
        screen.blit(bullet_img, (bullet[0], bullet[1]))

        if bullet[1] < -bullet_img.get_height():
            bullets.remove(bullet)

        for enemy in enemies:
            if bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_img.get_width():
                if bullet[1] > enemy[1] and bullet[1] < enemy



import pygame
import sys

# 初期化
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# プレイヤーの設定
player_x = 300
player_y = 400
player_speed = 5

# 弾の設定
bullet_width = 5
bullet_height = 10
bullet_speed = 10
bullets = []

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キーが押されている間、弾を発射し続ける
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bullet_x = player_x + 25
        bullet_y = player_y
        bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    # プレイヤーの移動
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed

    # 弾の移動
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # 描画
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, 50, 50))
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)
    pygame.display.update()

    # フレームレートの設定
    clock.tick(60)



# Time setting of boss
waiting_time = 0
boss_delay = 5000

running = True
while running:
    # Process the events
    screen.fill((0, 0, 0))

    # Draw boss
    if score >= 100:
        waiting_time += pygame.time.get_delta()
        if waiting_time >= boss_delay:
            bosses.draw(screen)
            bosses.update()
        else:
            # Display a message to indicate waiting time
            font = pygame.font.Font(None, 36)
            text = font.render("Boss will appear in {} seconds".format((boss_delay - waiting_time) // 1000 + 1), True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

    # Other game logic and drawing

    pygame.display.flip()
    clock.tick(FPS)

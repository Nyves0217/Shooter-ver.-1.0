import pygame
import random
import csv
pygame.init()

#Basic setup
SCREEN_WIDTH = 800
ROWS = 31
MAX_COLS = 50
SCREEN_HEIGHT = 640
TILE_SIZE = SCREEN_HEIGHT // ROWS
tile_types = 6
src = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

#variables-I
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.75
bullet_img = pygame.image.load("ZAssets/Attack related/Point/0.png").convert_alpha()
MC_idle = "MC_idle"
Enemy_idle = "Antagonist"
colors = {
    "pink" : (255, 192, 203, 1),
    "purple" : (160, 32, 240, 1),
    "blue" : (135, 206, 235, 1),
    "green" : (0, 255, 0, 1),
    "red": (255, 0, 0),
    "white" : (255, 255, 255)
}
level_colors = [colors["pink"]]


image = pygame.image.load("ZAssets/background related/bg.png")
rect = image.get_rect()

#variables-II
moving_left = False
moving_right = False
shoot = False
m2 = False
flung = False
tossed = False
user = False
level = 1

#variables-III
item_box_img = pygame.image.load("ZAssets/background related/box.png")
health_box_img = pygame.image.load("ZAssets/background related/h_box.png")
boxes = {
    "Health" : health_box_img,
    "Ammo" : item_box_img
}
font = pygame.font.SysFont("Roboto", 20)
rows = 23
cols = 50
img_list = []
for x in range(1, tile_types):
    img = pygame.image.load(f"ZAssets/background related/Stuff/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
tile_size = SCREEN_HEIGHT // rows


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    src.blit(img, (x, y))


#classes
class Soldier(pygame.sprite.Sprite):
    def __init__(self, main_folder, directory, directory2, scale, x, y, speed, limit, limit2, hp, ammo, ammo2):
        self.hp = hp
        self.maxhp = self.hp
        self.alive = True
        self.speed = speed
        self.flip = False
        self.in_air = False
        self.direction = 1
        pygame.sprite.Sprite.__init__(self)
        self.cooldown = 0
        self.imgs = []
        self.ammo = ammo
        self.ammo2 = ammo2
        self.ammo2_start = self.ammo2
        self.index = 0
        self.action = 0
        self.vel_y_comp = 0
        self.dx = 0
        self.dy = 0
        self.jump = False
        temp_list = []
        for i in range(0, limit):
            img = pygame.image.load(f"ZAssets/{main_folder}/{directory}/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.imgs.append(temp_list)
        temp_list = []
        for i in range(0, limit2):
            img = pygame.image.load(f"ZAssets/{main_folder}/{directory2}/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.imgs.append(temp_list)
        self.dead_img = pygame.image.load("ZAssets/Death/0.png")
        self.image = self.imgs[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_time = pygame.time.get_ticks()
        #ai specific
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 120, 40)
        #MC specific
        self.index2 = 0
        self.bullet_sequence = []
        for i in range(0, 5):
            image = pygame.image.load(f"ZAssets/MC related/Ammo/{i}.png")
            image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
            self.bullet_sequence.append(image)
        self.moving_bullet_sequence = []
        self.index3 = 0
        for i in range(0, 5):
            image2 = pygame.image.load(f"ZAssets/MC related/moving_ammo/{i}.png")
            image2 = pygame.transform.scale(image2, (image2.get_width() * scale, image2.get_height() * scale))
            self.moving_bullet_sequence.append(image2)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def move(self, moving_left, moving_right):
        self.dx = 0
        self.dy = 0
        if moving_left:
            self.dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            self.dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump and self.in_air == False:
            self.vel_y_comp = -14
            self.jump = False
            self.in_air = True
        self.vel_y_comp += GRAVITY
        self.dy += self.vel_y_comp
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                if self.vel_y_comp < 0:
                    self.vel_y_comp = 0
                    self.dy = tile[1].bottom - self.rect.top
                elif self.vel_y_comp >= 0:
                    self.vel_y_comp = 0
                    self.in_air = False
                    self.dy = tile[1].top - self.rect.bottom
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update_animation(self):
        Cooldown = 100
        if self.index >= len(self.imgs[self.action]):
            self.index = 0
            self.action = 0
        self.image = self.imgs[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > Cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False
            self.image= self.dead_img
            self.rect.y -= 10
            if self.rect.y <= -50:
                self.kill()

    def shoot(self, dir, condition, movingleft, movingright):
        COOLDOWN = 50
        if condition and self.ammo > 0 and (movingleft == False and movingright == False):
            if self.index2 >= len(self.bullet_sequence):
                self.index2 = 0
            self.image = self.bullet_sequence[self.index2]
            if pygame.time.get_ticks() - self.update_time > COOLDOWN:
                self.index2 += 1
                self.update_time = pygame.time.get_ticks()
        if condition and self.ammo > 0 and (movingleft or movingright):
            if self.index3 >= len(self.moving_bullet_sequence):
                self.index3 = 0
            self.image = self.moving_bullet_sequence[self.index3]
            if pygame.time.get_ticks() - self.update_time > COOLDOWN:
                self.index3 += 1
                self.update_time = pygame.time.get_ticks()
        if self.cooldown == 0 and self.ammo > 0:
            self.cooldown = 25
            if condition:
                b = Bullet(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction) + (13 * self.direction), self.rect.centery + 5, self.direction, f"{dir}")
                bullet_group.add(b)
                self.ammo -= 1
            else:
                b2 = EnemyBullet(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction) + (13 * self.direction), self.rect.centery, self.direction, f"{dir}")
                bullet_group.add(b2)
                self.ammo -= 1

    def draw(self):
        src.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.cooldown > 0:
            self.cooldown -= 1

    def AI(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot("Point", False, True, True)
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    if self.move_counter > tile_size:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, dir):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load(f"ZAssets/Attack related/{dir}/0.png")
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += self.direction * self.speed
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        for player2 in enemy_group:
            if pygame.sprite.spritecollide(player2, bullet_group, False):
                if player2.alive:
                    player2.hp -= 15
                    self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, dir):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load(f"ZAssets/Attack related/{dir}/0.png")
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.center = (x, y)
    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.hp -= 5
                self.kill()



class DD(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 50
        self.vel_ycomp = -11
        self.vel_xcomp = 7
        self.speed = 10
        self.image = pygame.image.load(f"ZAssets/Attack related/Point/1.png")
        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.vel_ycomp += GRAVITY
        dx = self.vel_xcomp * self.direction
        dy = self.vel_ycomp
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.vel_xcomp
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.vel_xcomp = 0
                if self.vel_ycomp < 0:
                    self.vel_ycomp = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_ycomp >= 0:
                    self.vel_ycomp = 0
                    dy = tile[1].top - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y)
            explosion_group.add(explosion)
            if abs(self.rect.centerx - player.rect.centerx) < tile_size * 2 and abs(self.rect.centery - player.rect.centery) < tile_size:
                player.hp -= 50
            for player2 in enemy_group:
                if abs(self.rect.centerx - player2.rect.centerx) < tile_size * 2 and abs(self.rect.centery - player2.rect.centery) < tile_size:
                    player2.hp -= 50


class Item_box(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = boxes[type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + (tile_size // 2), y + (tile_size - self.image.get_height()))

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if self.type == "Health":
                player.hp += 25
                if player.hp > player.maxhp:
                    player.hp = player.maxhp
            elif self.type == "Ammo":
                player.ammo += 5
                player.ammo2 += 2
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = []
        for i in range(0, 20):
            self.image = pygame.image.load(f"ZAssets/Attack related/Explosion/{i}.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
            self.imgs.append(self.image)
        self.index = 0
        self.image = self.imgs[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.imgs):
                self.kill()
            else:
                self.image = self.imgs[self.index]


class Healthbar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.health = hp
        self.max_health = max_hp

    def draw(self, health):
        self.health = health
        ratio = player.hp / player.maxhp
        pygame.draw.rect(src, colors["purple"], (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(src, colors["red"], (self.x, self.y, 150, 20))
        pygame.draw.rect(src, colors["pink"], (self.x, self.y, 150 * ratio, 20))


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                img = img_list[tile]
                img_rect = img.get_rect()
                img_rect.x = x * TILE_SIZE
                img_rect.y = y * TILE_SIZE
                tile_data = (img, img_rect)
                if tile == 0:
                    self.obstacle_list.append(tile_data)
                elif tile == 1:
                    i_box = Item_box("Ammo", x * TILE_SIZE, y * TILE_SIZE)
                    box_group.add(i_box)
                elif tile == 2:
                    h_box = Item_box("Health", x * TILE_SIZE, y * TILE_SIZE)
                    box_group.add(h_box)
                elif tile == 3:
                    player = Soldier("MC related", MC_idle, "MC animation", 2, x * TILE_SIZE, y * TILE_SIZE, 3, 2, 5, 300, 20000, 10)
                    health_bar = Healthbar(10, 10, player.hp, player.hp)
                elif tile == 4:
                    player2 = Soldier("Enemies related", Enemy_idle, "Enemy animation", 2, x * TILE_SIZE, y * TILE_SIZE, 2, 2, 5, 50,90, 10)
                    enemy_group.add(player2)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            src.blit(tile[0], tile[1])

#instances/groups
enemy_group = pygame.sprite.Group()
DD_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
b2_group = pygame.sprite.Group()
s_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()

world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

with open(f"level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)
#main loop
run = True
while run:
    src.fill(colors["blue"])
    src.blit(image, rect)
    clock.tick(FPS)
    world.draw()
    health_bar.draw(player.hp)
    draw_text(f"Bullets: {player.ammo}", font, colors["white"], 10, 35)
    draw_text(f"Bombs: {player.ammo2}", font, colors["white"], 10, 50)
    player.draw()
    player.update()

    for player2 in enemy_group:
        player2.draw()
        player2.update()
        if player2.alive:
            player2.AI()
    bullet_group.update()
    b2_group.update()
    DD_group.update()
    b2_group.draw(src)
    explosion_group.update()
    bullet_group.draw(src)
    DD_group.draw(src)
    explosion_group.draw(src)
    box_group.update()
    box_group.draw(src)
    if player.alive:
        if shoot:
            player.shoot("Point", True, moving_left, moving_right)
        elif flung and tossed == False and player.ammo2 > 0:
            if player.direction == 1:
                dd = DD(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction) + 11, player.rect.centery - 17, player.direction)
            else:
                dd = DD(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction) - 11, player.rect.centery - 17,
                        player.direction)
            DD_group.add(dd)
            player.ammo2 -= 1
            tossed = True
        if moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_e:
                flung = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_e:
                flung = False
                tossed = False
    pygame.display.update()

pygame.quit()
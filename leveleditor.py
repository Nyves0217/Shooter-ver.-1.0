import pygame
import csv
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300


ROWS = 31
font = pygame.font.SysFont("Arial", 30)
darkness = (0, 0, 0)
level = 1
MAX_COLS = 50
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 6
clock = pygame.time.Clock()
FPS = 60

world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0



src = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level editor")
src_color = (230, 230, 250)
line_color = (255, 255, 255)
background = pygame.image.load("ZAssets/background related/bg.png")
Highlight_color = (255, 0, 0, 1)

current_tile = 0

char_list = []
for i in range(1, TILE_TYPES):
    img = pygame.image.load(f"ZAssets/background related/Stuff/{i}.png")
    if img != pygame.image.load(f"ZAssets/background related/Stuff/5.png") and img != pygame.image.load(f"ZAssets/background related/Stuff/{i}.png"):
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    else:
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
    char_list.append(img)

save_btn = pygame.image.load("ZAssets/Res_button/3.png")
load_btn = pygame.image.load("ZAssets/Res_button/4.png")


class Button():
    def __init__(self, x, y, image, scale):
        self.image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        src.blit(self.image, (self.rect.x, self.rect.y))
        return action


button_list = []
save_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_btn, 1)
load_button = Button(SCREEN_WIDTH//2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_btn, 1)
button_col = 0
button_row = 0
for i in range(len(char_list)):
    if i != 4:
        tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, char_list[i], 1)
    else:
        tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, char_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    src.blit(img, (x, y))


def draw_bg():
    src.fill(src_color)
    src.blit(background, (0, SCREEN_HEIGHT - background.get_height()))


def draw_grid():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(src, line_color, (c * TILE_SIZE, 0), (c * TILE_SIZE, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(src, line_color, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


def draw_world():
    for j, row in enumerate(world_data):
        for i, tile in enumerate(row):
            if tile >= 0:
                src.blit(char_list[tile], (i * TILE_SIZE, j * TILE_SIZE))

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()
    if save_button.draw():
        with open(f"level{level}_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in world_data:
                writer.writerow(row)
    draw_text(f"Level: {level}", font, darkness, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    if load_button.draw():
        with open(f"level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    pygame.draw.rect(src, src_color, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    button_count = 0
    pos = pygame.mouse.get_pos()
    x, y = (pos[0]) // TILE_SIZE, (pos[1]) // TILE_SIZE
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1
    for button_count, i in enumerate(button_list):
        if i.draw():
            current_tile = button_count
    pygame.draw.rect(src, Highlight_color, button_list[current_tile].rect, 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and level >= 1:
            if event.key == pygame.K_UP and level > 0:
                level += 1
            if event.key == pygame.K_DOWN:
                level -= 1
    pygame.display.update()
pygame.quit()

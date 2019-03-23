import sys
import os
import random
import pygame

size = WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode(size)
FPS = 50

clock = pygame.time.Clock()
pygame.init()
pygame.key.set_repeat(1, 5)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image
 
def terminate():
    pygame.quit()
    sys.exit()
 
def start_screen():
    intro_text = ["Игра Pong.",
                  "Надо отбивать мяч, чтобы не проиграть."]
    
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)
        
def end_screen():
    intro_text = ["Game Over"]
    
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50) 
    text_coord = 50
    
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 245
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


class Ball(pygame.sprite.Sprite):
    def __init__(self, rad, x, y):
        super().__init__(all_sprites)
        self.rad = rad
        self.image = pygame.Surface((2 * rad, 2 * rad), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('#ffff00'), (rad, rad), rad)
        self.rect = pygame.Rect(x, y, 2 * rad, 2 * rad)
        self.vx = 4
        self.vy = 6
        
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, platform):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, game_over_border):
            self.vy = 0
            self.vx = 0
            end_screen()
            

class Platform(pygame.sprite.Sprite):
    size = (100, 15)
    
    def __init__(self, pos):
        super().__init__(all_sprites)    
        self.add(platform)
        self.image = pygame.Surface(Platform.size)
        self.image.fill(pygame.Color("#0f00ff"))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_event(self, key):
        if key[pygame.K_RIGHT]:
            self.rect.x += 10
        elif key[pygame.K_LEFT]:
            self.rect.x -= 10

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if y1 != HEIGHT:
            if x1 == x2:
                self.add(vertical_borders)
                self.image = pygame.Surface([0, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 0, y2 - y1)
            else:
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 0])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 0)
        else:
            self.add(game_over_border)
            self.image = pygame.Surface([x2 - x1, 0])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 0)


all_sprites = pygame.sprite.Group()

platform = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
game_over_border = pygame.sprite.Group()

Border(0, 0, WIDTH, 0)
Border(0, HEIGHT, WIDTH, HEIGHT)
Border(0, 0, 0, HEIGHT)
Border(WIDTH, 0, WIDTH, HEIGHT)

ball = Ball(12, 342, 450)
plfrm = Platform((300, 475))

start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            plfrm.get_event(key)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
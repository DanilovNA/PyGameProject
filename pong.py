import os
import random
import pygame

size = width, height = 700, 500
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

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


class Ball(pygame.sprite.Sprite):
    def __init__(self, rad, x, y):
        super().__init__(all_sprites)
        self.rad = rad
        self.image = pygame.Surface((2 * rad, 2 * rad), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('#ffff00'), (rad, rad), rad)
        self.rect = pygame.Rect(x, y, 2 * rad, 2 * rad)
        self.vx = 2
        self.vy = 2
        
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, platform):
            self.vy = -self.vy

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
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


all_sprites = pygame.sprite.Group()

platform = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

Border(0, 0, width, 0)
Border(0, height, width, height)
Border(0, 0, 0, height)
Border(width, 0, width, height)

ball = Ball(12, 342, 450)
plfrm = Platform((300, 475))

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
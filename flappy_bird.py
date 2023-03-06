import pygame
import sys
import random
import os


#遊戲初始化 和 創建視窗
screen_width = 600
screen_high = 800

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_high))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 100


#載入圖片
background_img = pygame.image.load(os.path.join("img", "背景.png")).convert()
bird_img = pygame.image.load(os.path.join("img", "bird.png")).convert()
pipedown_img = pygame.image.load(os.path.join("img", "水管下.png")).convert()
pipeup_img = pygame.image.load(os.path.join("img", "水管上.png")).convert()


#障礙物
gap = 250

pipe_width = 500
pipe_high = 500

pipe_x_init = 480
pipedown_y = 450
pipe_x = pipe_x_init
pipeup_y = pipedown_y - gap - pipe_high

#水管下
class Pipedown(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pipedown_img,(pipe_width,pipe_high ))
        self.image.set_colorkey((0,0,0)) 
        self.rect = self.image.get_rect()
        self.rect.x = pipe_x_init
        self.rect.y = pipedown_y

    def update(self):
        self.rect.x = pipe_x
        self.rect.y = pipedown_y
#水管上
class Pipeup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pipeup_img,(pipe_width,pipe_high))
        self.image.set_colorkey((0,0,0)) 
        self.rect = self.image.get_rect()
        self.rect.x = pipe_x
        self.rect.y = -600

    def update(self):
        self.rect.x = pipe_x
        self.rect.y = pipeup_y
        
#鳥
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bird_img,(65,65))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 220
        self.rect.centery = 400
        self.jumped = False
        self.vel_y = 0
    def update(self):
        y_move = 0
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and self.jumped is False:
            self.vel_y = -11
            self.jumped = True
        if not key_pressed[pygame.K_SPACE]:
            self.jumped = False

        self.vel_y +=0.4
        if self.vel_y > 8:
            self.vel_y = 8
        y_move += self.vel_y
        self.rect.y += y_move

        if self.rect.y < 0:
            self.rect.y = 0


all_sprites = pygame.sprite.Group()

pipedown = Pipedown()
all_sprites.add(pipedown)

pipeup = Pipeup()
all_sprites.add(pipeup)

bird = Bird()
all_sprites.add(bird)


#遊戲主迴圈
running = True
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
         
        
    #遊戲畫面更新
    pipe_x += -2.6

    if pipe_x<-370:
        pipe_x = pipe_x_init
        pipedown_y = random.randrange(300,700)
        pipeup_y = pipedown_y - gap - pipe_high

    all_sprites.update()
    hitup = pygame.sprite.collide_mask(bird,pipeup)
    if hitup:
        running = False
    hitdown = pygame.sprite.collide_mask(bird,pipedown) 
    if hitdown:
        running = False
          
    #畫面顯示
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()


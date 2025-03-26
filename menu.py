# importaciones del juego
import pygame, random
# enrutamiento de imagenes y archivos en la carpeta assets
import os

# TAMAÑO DEL LIENZO
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)
RED = (255,0,0)
ROOT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(ROOT_DIR, 'assets')
VIDAS = 3


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GALAGA')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_DIR,'player.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10 
        self.speed_x = 0
        
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_DIR,'meteorGrey_big1.png'))
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5) 
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > HEIGHT + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)
            
class Disparos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((7,25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = -10  
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  
            self.kill()

def mostrar_texto(texto,x,y,color=WHITE):
    render = font.render(texto,True,color)
    screen.blit(render, (x, y))


background = pygame.image.load(os.path.join(IMAGE_DIR,'background.gif')).convert()

pygame.font.init()
font = pygame.font.Font(None,36)
        
    
all_sprites = pygame.sprite.Group()
nave = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
disparo = pygame.sprite.Group()


player = Player()
nave.add(player)
all_sprites.add(player)

for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                disparo1 = Disparos(player.rect.centerx, player.rect.top)
                all_sprites.add(disparo1) 
                disparo.add(disparo1)  
            
    all_sprites.update()

    colisionM=pygame.sprite.groupcollide(disparo,meteor_list,True,True)

    for colisionesM in colisionM:
        nuevo_meteorito = Meteor()
        all_sprites.add(nuevo_meteorito)
        meteor_list.add(nuevo_meteorito) 


    colisionN=pygame.sprite.groupcollide(nave,meteor_list,False,True)

    for colisionesN in colisionN:
        nuevo_meteorito = Meteor()
        all_sprites.add(nuevo_meteorito)
        meteor_list.add(nuevo_meteorito) 

    if colisionN:
        VIDAS -=1
    
    if VIDAS == 0:
        running = False
    
    screen.blit(background, [0,0])
    mostrar_texto(f"Vidas: {VIDAS}", 0, 0)
    
    all_sprites.draw(screen)
    
    pygame.display.flip()
    
pygame.quit()
from pygame import *
from random import randint
window = display.set_mode((700, 700))
display.set_caption('Kick monster👽')
background = transform.scale(image.load('galaxy.jpg'), (700, 700))
game = True
FPS = 60
clock = time.Clock()
mixer.init()
font.init()
w = mixer.Sound('win.ogg')
l = mixer.Sound('lose.ogg')
mixer.music.load('звуккосмоса.ogg')
mixer.music.play()
finish = False
class Game_sprite(sprite.Sprite):
    def __init__ (self, player_x, player_y, player_speed, player_image, x, y):
        super().__init__()
        self.image = sprite1 = transform.scale(image.load(player_image), (x, y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class player(Game_sprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -=  self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
    def bulet(self):
        bullet = Bullet(self.rect.centerx - 17, self.rect.y, 6, 'патрон.png', 35, 50)
        bullets.add(bullet)
class Enemy(Game_sprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = -50
            lost += 1
class Asteroid(Game_sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = -50
class Bullet(Game_sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
sprite1 = player(330, 600, 5, 'кос_корабль.png', 100, 100)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy(randint(50, 650), -50, randint(1, 4), 'злодей.png', 100, 70)
    monsters.add(monster)
for i in range(1):
    asteroid = Asteroid(randint(50, 650), -50, randint(1, 4), 'asteroid.png', 100, 70)
    asteroids.add(asteroid)
lost = 0
kill = 0
while game:
    if not finish:
        window.blit(background, (0, 0))
        kill_mosters = font.SysFont('Arial', 35,).render('Счёт:' + str(kill), True, (255, 0, 0))
        monsters.update()
        monsters_lost = font.SysFont('Arial', 35,).render('Пропущено:' + str(lost), True, (255, 0, 0))
        window.blit(monsters_lost, (1, 75))
        window.blit(kill_mosters, (1, 50))
        sprite1.reset()
        monsters.draw(window)        
        asteroids.draw(window)        
        bullets.update()     
        asteroids.update()     
        bullets.draw(window)        
        sprite1.move()
        if kill >= 10:
            win = font.SysFont('Arial', 60,).render('Вы выиграли! Ваш счёт:' + str(kill), True, (255, 0, 0))
            window.blit(win,(50, 240))
            finish = True
            w.play()
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        sprite_list2 = sprite.spritecollide(sprite1, asteroids, True)
        #print(sprite_list2)
        for i in sprite_list:
            monster = Enemy(randint(50, 650), -50, randint(1, 4), 'злодей.png', 100, 70)
            monsters.add(monster)
            kill += 1
        if lost >= 3 or len(sprite_list2) == 1:
            lose = font.SysFont('Arial', 70,).render('Вы проиграли!', True, (255, 0, 0))
            window.blit(lose,(130, 240))
            finish = True
            l.play()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                sprite1.bulet()
                mixer.init()
                fire = mixer.Sound('выстрел.ogg')               
                fire.play()
    display.update()
    clock.tick(FPS)

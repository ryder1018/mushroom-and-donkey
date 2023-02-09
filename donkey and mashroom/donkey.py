import sys
import pygame
import random
import os


fps = 60
boss_score = 50000
black = (0,0,0)
SCREENWIDTH = 1000
SCREENHEIGHT = 800
GREEN = (0,255,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
PLAYERWIDTH  = 200
PLAYERHEIGHT = 500
#遊戲初始化和創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('驢子採香菇')


#import img
donkeys = pygame.image.load(os.path.join("img", "donkey_talk.png")).convert()
donkey_talk = pygame.transform.scale(donkeys, (1000,800))
bosss = pygame.image.load(os.path.join("img", "boss_talk.png")).convert()
boss_talk = pygame.transform.scale(bosss,(1000,800))
backgrounds_img = pygame.image.load(os.path.join("img", "background.jpeg")).convert() #convert用意為轉化成pygame易讀取之
background_img = pygame.transform.scale(backgrounds_img,(2000,900))
player_img = pygame.image.load(os.path.join("img", "donkey.jpg")).convert() 
dreamcatcher_img = pygame.image.load(os.path.join("img", "dreamcatcher.jpg")).convert() 
mushroom0s_img = pygame.image.load(os.path.join("img", "mushroom0.jpg")).convert()  
mushroom1s_img = pygame.image.load(os.path.join("img", "mushroom1.jpg")).convert()  
mushroom2s_img = pygame.image.load(os.path.join("img", "mushroom2.jpg")).convert() 
mushroom0_img = pygame.transform.scale(mushroom0s_img,(180,168))
mushroom1_img = pygame.transform.scale(mushroom1s_img,(180,168))
mushroom2_img = pygame.transform.scale(mushroom2s_img,(180,168))
mushroom_imgs = [mushroom0_img, mushroom1_img, mushroom2_img]
pygame.display.set_icon(player_img)
boss_img = pygame.image.load(os.path.join("img", "boss.png")) 
power_imgs = {}
p11 = pygame.image.load(os.path.join("img", "shield.jpg")).convert()
p1 = pygame.transform.scale(p11,(160,160))
p22 = pygame.image.load(os.path.join("img", "attack.jpg")).convert()  
p2 = pygame.transform.scale(p22,(160,160))
power_imgs['shield'] = p1
power_imgs['gun'] = p2
    #anime
expl_mov = {}
expl_mov['lg'] = []
expl_mov['sm'] = []
expl_mov['player'] = []
for i in range(3):
    expl_img=pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(black)
    expl_mov['lg'].append(pygame.transform.scale(expl_img, (150, 150)))
    expl_mov['sm'].append(pygame.transform.scale(expl_img, (75, 75)))
    player_expl_imgs = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert() 
    player_expl_img = pygame.transform.scale(player_expl_imgs, (280,350))
    player_expl_img.set_colorkey(black)
    #expl_mov['player'].append(expl_img)
    expl_mov['player'].append(player_expl_img)
    

#import music
shoot_sound = pygame.mixer.Sound(os.path.join("music", "shoot.wav")) 
shield_sound = pygame.mixer.Sound(os.path.join("music", "pow0.mp3")) 
manyshoot_sound = pygame.mixer.Sound(os.path.join("music", "pow1.mp3")) 
expl_sounds = [pygame.mixer.Sound(os.path.join("music", "expl.wav")), pygame.mixer.Sound(os.path.join("music", "expl2.wav"))]

pygame.mixer.music.load(os.path.join("music", "background_music.mp3"))
pygame.mixer.music.set_volume(0.65)

die_sound = pygame.mixer.Sound(os.path.join("music", "player_expl.wav"))

font_name = os.path.join('Running_Script.ttf')
def draw_text(surf, text, size, x, y):          #繪畫
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_mushroom():
    m = Mushroom()          #產生香菇
    all_sprites.add(m)  #要加回all sprites才能繼續update and draw
    mushrooms.add(m) #才能加回群組繼續判

def draw_health(surf,all_health, hp, x, y,bar_length, color):                #血量格
    if hp < 0:
        hp = 0
    BAR_LENGTH = bar_length
    BAR_HEIGHT = 10
    fill = (hp/all_health) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf,color,fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)#2 repersent幾像素   


def draw_init():    #主頁面                   
    screen.fill((0,0,0))
    screen.blit(background_img, (0,0))
    draw_text(screen, '驢子大戰香菇', 64, SCREENWIDTH/2, SCREENHEIGHT/2)
    draw_text(screen, 'w,s or 上下鍵控制驢子', 32, SCREENWIDTH/2, SCREENHEIGHT*3/4)
    draw_text(screen, '空白鍵開始', 32, SCREENWIDTH/2, 200)
    draw_text(screen, '以空白鍵發射捕夢網', 32, SCREENWIDTH/2, SCREENHEIGHT*5/6+7)
    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    draw_init1()
                   
                    
def draw_init1():
    screen.fill((0,0,0))
    screen.blit(background_img, (0,0))
    draw_text(screen, '魔王打越久，分數越高', 32, SCREENWIDTH/2, SCREENHEIGHT/2+80)
    draw_text(screen, '製作者：吳宇藤', 32, SCREENWIDTH/2, SCREENHEIGHT*3/4)
    draw_text(screen, '空白鍵繼續', 32, SCREENWIDTH/2, 200)
   
    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False      
                    draw_init2()        

def draw_init2():

    screen.fill((0,0,0))
    screen.blit(donkey_talk, (0,0))
    draw_text(screen, '我是驢子，那是武器：捕夢網，按空白鍵發射子彈！', 32, SCREENWIDTH/2-100, 100)

   
    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False  
                    draw_init3()
                    
def draw_init3():
    screen.fill((0,0,0))
    screen.blit(boss_talk, (0,0))
    draw_text(screen, '我是大魔王，這是香菇', 32, SCREENWIDTH/2-100, 100)
    draw_text(screen, '我們要去攻擊驢子和捕夢網！！', 32, SCREENWIDTH/2-100, 170)

   
    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False  
                    draw_init4()

def draw_init4():
    screen.fill((0,0,0))
    screen.blit(donkey_talk, (0,0))
    draw_text(screen, '我要去打爆大魔王', 32, SCREENWIDTH/2-100, 100)

   
    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False  


def show_end_menu():
    screen.fill((0,0,0))
    screen.blit(background_img, (0,0))
    draw_text(screen, '恭喜你，勇者', 32, SCREENWIDTH/2, SCREENHEIGHT/2-30)
    draw_text(screen, '你戰勝了這個遊戲', 32, SCREENWIDTH/2, SCREENHEIGHT/2+30)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    show_end_menu1()
                    
def show_end_menu1():
    screen.fill((0,0,0))
    screen.blit(background_img, (0,0))
    draw_text(screen,'真是厲害呢',32,SCREENWIDTH/2,SCREENHEIGHT/2+50)
    draw_text(screen,'你總共得到了'+str(score)+'分',32,SCREENWIDTH/2,SCREENHEIGHT/2-50)    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False    
                    show_end_menu2()

def show_end_menu2():
    screen.fill((0,0,0))
    screen.blit(donkey_talk, (0,0))
    draw_text(screen,'耶耶我贏了',32,SCREENWIDTH/2-100,100)    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False 
                    show_end_menu3() 

def show_end_menu3():
    screen.fill((0,0,0))
    screen.blit(boss_talk, (0,0))
    draw_text(screen,'喔不喔不喔不不不不～～～',32,SCREENWIDTH/2-100,100)   
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False  
                    draw_init()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image =  pygame.transform.scale(boss_img, (100,500))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = 890
        self.rect.y = SCREENHEIGHT - 1
        self.speedy = 10
        self.speedx = -10
        self.health = 1000

    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.right < 800:
            self.rect.right = 800
            self.speedx = 10
        if self.rect.left >890:
            self.rect.left = 890
            self.speedx = -10
        
        if self.rect.top > SCREENHEIGHT:
            self.rect.y == SCREENHEIGHT
            self.speedy = -4
        if self.rect.bottom < 0:
            self.rect.y == 0
            self.speedy = 4

    def boss_shoot(self):
        if boss.health>800:
            boss_bullet = Boss_bullet(self.rect.left, self.rect.centery)
            all_sprites.add(boss_bullet)
            boss_bullets.add(boss_bullet)
        if boss.health>300 and boss.health <= 800:
            boss_bullet1 = Boss_bullet(self.rect.left, self.rect.top)
            boss_bullet2 = Boss_bullet(self.rect.left, self.rect.bottom)
            all_sprites.add(boss_bullet1)
            all_sprites.add(boss_bullet2)
            boss_bullets.add(boss_bullet2)
            boss_bullets.add(boss_bullet1)
        if boss.health<= 300:
            boss_bullet0 = Boss_bullet(self.rect.left, self.rect.centery)
            boss_bullet1 = Boss_bullet(self.rect.left,self.rect.bottom-4)
            boss_bullet2 = Boss_bullet(self.rect.left, self.rect.top+4)
            all_sprites.add(boss_bullet0)
            all_sprites.add(boss_bullet1)
            all_sprites.add(boss_bullet2)
            boss_bullets.add(boss_bullet0)
            boss_bullets.add(boss_bullet1)
            boss_bullets.add(boss_bullet2)

class Boss_bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.speedx = random.randrange(-25, -20)
        self.speedy = random.randrange(-5,5)

    
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()
        
        if score > boss_score + 15000:
            self.rect.centery += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > SCREENHEIGHT:
            self.kill()
    


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (210,280))
        self.image.set_colorkey(black )
        self.rect = self.image.get_rect()
        self.radius = 105
        #pygame.draw.circle(self.image,RED, self.rect.center, self.radius)
        self.rect.x = 100
        self.rect.y = 400
        self.speedy = 10
        self.health = 100
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun >1 and now - self.gun_time > 2000:
            self.gun -=1
            self.gun_time = now
        key_pressed = pygame.key.get_pressed()  #會回傳給我們亦整串boolin,represent每一個鍵盤是否按壓
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedy

        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy

        if self.rect.top < 0:           #中心點無法超越螢幕
            self.rect.top = 0
        if self.rect.bottom > SCREENHEIGHT:
            self.rect.bottom = SCREENHEIGHT
        

        #if self.rect.bottom < 0:            #讓他超過螢幕可以從反方向回來
        #   self.rect.top = SCREENHEIGHT       
        #if self.rect.top > SCREENHEIGHT:
        #    self.rect.bottom = 0
    
    def shoot(self):
        if self.gun == 1:
            dreamcatcher = Dreamcatcher(self.rect.right, self.rect.centery)
            all_sprites.add(dreamcatcher)
            dreamcatchers.add(dreamcatcher)
            shoot_sound.play()
        elif self.gun >=2 and self.gun<=4 :
            dreamcatcher1 = Dreamcatcher(self.rect.centerx, self.rect.top)
            dreamcatcher2 = Dreamcatcher(self.rect.centerx, self.rect.bottom)
            all_sprites.add(dreamcatcher1)
            all_sprites.add(dreamcatcher2)
            dreamcatchers.add(dreamcatcher1)
            dreamcatchers.add(dreamcatcher2)
            shoot_sound.play()
        elif self.gun > 4 :
            dreamcatcher1 = Dreamcatcher(self.rect.centerx, self.rect.top)
            dreamcatcher2 = Dreamcatcher(self.rect.centerx, self.rect.bottom)
            dreamcatcher3 = Dreamcatcher(self.rect.centerx, self.rect.centery)
            all_sprites.add(dreamcatcher1)
            all_sprites.add(dreamcatcher2)
            all_sprites.add(dreamcatcher3)
            dreamcatchers.add(dreamcatcher1)
            dreamcatchers.add(dreamcatcher2) 
            dreamcatchers.add(dreamcatcher3)
        

    
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Mushroom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(mushroom_imgs)

        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.82/ 2)
        #pygame.draw.circle(self.image,RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(SCREENWIDTH+150, SCREENWIDTH+230)
        self.rect.y = random.randrange(10,SCREENHEIGHT - 10)
        self.speedx = random.randrange(5,15)
        self.speedy = random.randrange(-4,4) 

    def update(self):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > SCREENHEIGHT:                                              #讓香菇不斷反覆
            self.rect.x = random.randrange(SCREENWIDTH, SCREENWIDTH+100)
            self.rect.y = random.randrange(20,SCREENHEIGHT - 20)
            self.speedx = random.randrange(3,13)
            self.speedy = random.randrange(-2,2)

        if score >2000 and score<= 7000:
            self.speedx = random.randrange(10,15)
        if score >7000 and score<= 10000:
            self.speedx = random.randrange(13,18)
        if score > 10000 and score <=15000:
            self.speedx = random.randrange(15,20)
        if score >15000 and score <= 20000:
            self.speedx =random.randrange(17,22)
        if score > 20000 and score <= 25000:
            self.speedx =random.randrange(20,25)
        if score > 25000 and score <= 30000:        
            self.speedx = random.randrange(21,26)
        if score > 30000 and score <= 40000:        
            self.speedx = random.randrange(22,27)
        if score > 40000 and score <= 45000:        
            self.speedx = random.randrange(23,28)
        if score > 45000 and score <= 50000:        
            self.speedx = random.randrange(13,18)   #暴風雨前的寧靜


        if score >boss_score and score<= boss_score+15000:
            self.speedx = random.randrange(24,29)    #大魔王香菇速度
        if score >boss_score+15000:
            self.speedx = random.randrange(25,30)

        if player.health <= 0:      #讓驢子死亡後不會再遭被香菇打到
            self.speedx = 0
            self.speedy = 0
        if boss.health <=0:
            self.speedx = 0
            self.speedy = 0
        

class Dreamcatcher(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(dreamcatcher_img, (240,96))
        self.image.set_colorkey(black )
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.left = x
        self.speedx = 10


    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > SCREENWIDTH:
            self.kill()
        if self.rect.top > SCREENHEIGHT:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        if boss.health<= -10:  #防止魔王輸掉後玩家持續攻擊
            self.kill()

   
    
class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_mov[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0  #代表現在更新到第幾張圖片
        self.last_update = pygame.time.get_ticks()  #會回穿從初始化到現在經過的毫秒數
        self.frame_rate = 200    #至少經過幾毫秒才會到下一張圖片



    def update(self):
        now = pygame.time.get_ticks()                           #代表這個update被執行的時間
        if now - self.last_update > self.frame_rate:            
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_mov[self.size]):          #代表進入到最後一張了
                self.kill()
            else:
                self.image = expl_mov[self.size][self.frame]    #更新到下一張
                center = self.rect.center                       
                self.rect = self.image.get_rect()
                self.rect.center = center                       #重新定位到中心點

class Power(pygame.sprite.Sprite):

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(black )
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = random.randrange(-20,-15)


    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()


pygame.mixer.music.play(-1) #-1代表會無限播放

#game loop
running=True
show_init = True
while running:
    if show_init:            
        close =draw_init()
        if close:
            break
        show_init = False
        #以下為所有物件初始的動作
        all_sprites = pygame.sprite.Group()
        mushrooms = pygame.sprite.Group()
        dreamcatchers = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        boss = Boss()
        boss_bullets = pygame.sprite.Group()
        for i in range(11):
            new_mushroom()
        score = 0
    #


    clock.tick(fps)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                if score > boss_score:
                    boss.boss_shoot()
    


    #更新遊戲
    all_sprites.update()
        #捕夢網撞香菇
    hits = pygame.sprite.groupcollide(mushrooms,dreamcatchers,True ,True)  #first True判斷是否刪香菇，第二個判斷捕夢網
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius 
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.91:    #會random回傳0~1得直
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_mushroom()
        #香菇撞驢子
    hits = pygame.sprite.spritecollide(player, mushrooms, True, pygame.sprite.collide_circle)   #True判斷‘香菇’是否消失
    for hit in  hits:
        new_mushroom()
        player.health -= hit.radius /2.8
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0 :
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            die_sound.play() 
    if player.health<=0 and not(die.alive()):
        show_init = True
            
           
        
            
        #power撞驢子
    hits = pygame.sprite.spritecollide(player, powers, True) 
    for hit in hits:
        if hit.type == 'shield':
            player.health += 10
            if player.health > 100:
                player.health = 100
            shield_sound.play()

        elif hit.type == 'gun':
            player.gunup()
            manyshoot_sound.play()
    
    if score > boss_score:
        all_sprites.add(boss)
        

        #魔王子彈撞驢子
    hits = pygame.sprite.spritecollide(player, boss_bullets, True)
    for hit in hits:
        player.health -= 5
        if player.health <= 0:
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            die_sound.play()
            show_init = True
        #捕夢網撞大魔王子彈 
    pygame.sprite.groupcollide(dreamcatchers, boss_bullets, True,True)

        #捕夢網撞大魔王
    if score > boss_score:
        hits = pygame.sprite.spritecollide(boss, dreamcatchers, True)
        
        for hit in hits:
            boss.health -= 15
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if boss.health <= 0:
                die = Explosion(boss.rect.center, 'player')
                all_sprites.add(die)
                die_sound.play()
                #end_menu_init = True
        if boss.health <=0 and not(die.alive()):               
            show_end_menu()
            #end_menu_init = False
                
            #draw_init()
            #show_init = False
            #以下為所有物件初始的動作
            all_sprites = pygame.sprite.Group()
            mushrooms = pygame.sprite.Group()
            dreamcatchers = pygame.sprite.Group()
            powers = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            boss = Boss()
            boss_bullets = pygame.sprite.Group()
            for i in range(10):
                new_mushroom()
            score = 0
            #
                    
                                
                
              
    
        
    



    #畫面顯示
    screen.fill((black))
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, SCREENWIDTH-30, SCREENHEIGHT/2)
    draw_health(screen,100,player.health,5,SCREENHEIGHT / 2, 100,GREEN)
    if score > boss_score:
        draw_health(screen,1000, boss.health, 1,5, 1000,RED)  #第一個1000 represent boss血量 第二個代表血格長度
        draw_text(screen,'魔王血量',20,37,15)

    pygame.display.update()

pygame.quit()
import pygame as pg
import random as ran
pg.init() 
screen = pg.display.set_mode((800,600))
pg.display.set_caption('space invaders'.capitalize())
hero = pg.image.load('spaceship.png')
bg = pg.image.load('background1.png')
alien1 = pg.transform.rotate(pg.image.load('ufo.png'),180)
alien2 = pg.transform.rotate(pg.image.load('spake.png'),180)
alien3 = pg.transform.rotate(pg.image.load('alien.png'),180)
start_b = pg.image.load('power.png')
bullet = pg.image.load('bullet.png')
font = pg.font.SysFont('comic sans',30)
fontx = pg.font.SysFont('comic sans',50)
class Lazer:
    def __init__(self,x,y,img):
        self.x = x 
        self.y = y 
        self.img = img 
        self.mask = pg.mask.from_surface(self.img)
    def collision(self,obj):
        return collide(self,obj)
    def move(self,vel):
        self.y += vel
    def draw(self):
        screen.blit(self.img,(self.x,self.y))
    def off_screen(self,height):
        return not(self.y <= height and self.y >= 0)
class ship:
    def __init__(self,x,y,health=100):
        self.x = x 
        self.y = y 
        self.health = health 
        self.img = None 
        self.lazer = None
        self.lazers = []
        self.counter = 0
    def draw(self):
        for i in self.lazers:
            i.draw()
        screen.blit(self.img,(self.x,self.y))
    def movin_laz(self,vel,obj):
        self.cool()
        for i in self.lazers:
            i.move(vel)
            if i.off_screen(800):
                self.lazers.remove(i)
            elif i.collision(obj):
                obj.health -= 10
                self.lazers.remove(i)
    def cool(self):
        if self.counter >= 10:
            self.counter = 0
        elif self.counter > 0:
            self.counter += 1
    def shoot(self):
        if self.counter == 0:
            bul = Lazer(self.x+20,self.y,self.lazer)
            self.lazers.append(bul)
            self.counter = 1
class Player(ship):
    def __init__(self,x,y,img,score,health=100):
        super().__init__(x,y,health)
        self.img = img
        self.lazer = bullet
        self.mask = pg.mask.from_surface(self.img)
        self.max_health = health
        self.score = score
    def movin_laz(self,vel,objs):
        self.cool()
        for i in self.lazers:
            i.move(vel)
            if i.off_screen(800):
                self.lazers.remove(i)
            else:
                for obj in objs:
                    if i.collision(obj):
                        objs.remove(obj)
                        self.score += 1
                        self.lazers.remove(i)
    def draw(self, window):
        super().draw()
        self.healthbar(window)
    def healthbar(self, window):
        pg.draw.rect(window, (255,0,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))
        pg.draw.rect(window, (0,255,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.health/self.max_health), 10))
class Alien(ship):
    types = {
    'op':(alien1,pg.transform.rotate(bullet,180)),
    'mediocre':(alien2,pg.transform.rotate(bullet,180)),
    'weak':(alien3,pg.transform.rotate(bullet,180))
    }
    def __init__(self,x,y,typer,health=100):
        super().__init__(x,y,health)
        self.img,self.lazer = self.types[typer]
        self.mask = pg.mask.from_surface(self.img)
    def move(self,vel):
        self.y += vel
    def shoot(self):
        if self.counter== 0:
            lazer = Lazer(self.x+20, self.y, self.lazer)
            self.lazers.append(lazer)
            self.counter = 1
def collide(obj1,obj2):
    offset = (obj2.x - obj1.x, obj2.y - obj1.y)
    t_point = obj1.mask.overlap(obj2.mask,offset)
    if t_point:
        return True 
    return False
def main():
    player = Player(300,500,hero,0)
    level = 0
    lives = 10
    clock = pg.time.Clock()
    enemy = []
    group = 5
    run = True
    def redraw():
        score = player.score
        t1 = font.render(f'Level:{level}',1,(255,255,255))
        t2 = font.render(f'Score:{score}',1,(255,255,255))
        t3 = font.render(f'Lives:{lives}',1,(255,255,255))
        screen.blit(bg,(0,0))
        screen.blit(t1,(10,10))
        screen.blit(t2,(10,40))
        screen.blit(t3,(10,70))
        for i in enemy:
            i.draw()
        player.draw(screen)
        if len(player.lazers)!=0:
            player.movin_laz(-5,enemy)
        pg.display.update()
    while run:
        clock.tick(60)
        redraw()
        if lives == 0 or player.health == 0:
            lost = fontx.render('you lost'.capitalize(),1,(255,255,255))
            screen.blit(lost,(450-lost.get_width(),300-lost.get_height()))
            pg.display.flip()
            pg.time.delay(3000)
            run = False
        if len(enemy) == 0:
            group += 5
            level += 1
            for i in range(group):
                alienmate = Alien(ran.randint(100,700),ran.randint(-1000,-100),ran.choice(['op','mediocre','weak']))
                enemy.append(alienmate)
        for i in pg.event.get():
            if i.type == pg.QUIT:
                quit()
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and player.x > 0:
            player.x -= 2
        if key[pg.K_RIGHT] and player.x < 800 - player.img.get_width():
            player.x += 2
        if key[pg.K_UP] and player.y > 0:
            player.y -= 2
        if key[pg.K_DOWN] and player.y < 600 - player.img.get_height():
            player.y += 2
        if key[pg.K_SPACE]:
            player.shoot()
        for i in enemy:
            i.move(1)
            i.movin_laz(5,player)
            if ran.randrange(0, 2*60) == 1:
                i.shoot()
            if collide(i, player):
                player.health -= 10
                enemy.remove(i)
            if i.y > 600:
                lives -= 1
                enemy.remove(i)
    menu()
def menu():
    tb = fontx.render('start'.capitalize(),1,(255,255,255))
    while True:
        screen.blit(bg,(0,0))
        screen.blit(start_b,(430-start_b.get_width(),300-start_b.get_height()))
        screen.blit(tb,(435-tb.get_width(),300-start_b.get_height()+70))
        for i in pg.event.get():
            if i.type == pg.QUIT:
                quit()
            if i.type == pg.KEYDOWN:
                main()
        pg.display.flip()
menu()
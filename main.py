import pygame
import random


def checktouch(xa1, xa2, xb1, xb2, ya1, ya2, yb1, yb2):
    touch_x = False
    touch_y = False
    if (xb1 <= xa2) and (xb1 >= xa1):
        touch_x = True
    if (yb1 <= ya2) and (yb1 >= ya1):
        touch_y = True

    return touch_x and touch_y


class Plr:
    obj_type = 'player'

    def __init__(self, img, object_set, x=10, y=10, speed=1, xlen=25, ylen=35, ID=0, direction=1):
        self.ID = ID
        self.x = x
        self.xlen = xlen
        self.y = y
        self.ylen = ylen
        self.speed = speed
        self.direction = direction
        self.i = pygame.image.load(img)
        object_set.append(self)

    def move(self, x=0, y=0):
        if (self.x + x > 10) and (self.x + x < 460):
            if x > 0:
                self.direction = 1
                self.i = pygame.image.load('player.png')
            elif x < 0:
                self.direction = 2
                self.i = pygame.image.load('player1.png')
            self.x += x
        if (self.y + y > 10) and (self.y + y < 455):
            self.y += y

    def checkmoves(self, up, left, down, right):
        if up:
            self.move(y=(-1)*self.speed)
        elif left:
            self.move(x=(-1)*self.speed)
        elif down:
            self.move(y=self.speed)
        elif right:
            self.move(x=self.speed)

    def show(self, disp):
        disp.blit(self.i, (self.x, self.y))

    def collide(self, touch_object, touch_type):
        if self.ID == 1:
            c = counter1
        elif self.ID == 2:
            c = counter2

        if touch_type == 'apple':
            touch_object.eaten(c)


class Apple:
    count = 0
    obj_type = 'apple'

    def __init__(self, x, y, object_set, img='apple.png', ID=0, xlen=20, ylen=20):
        self.ID = ID
        self.x = x
        self.xlen = xlen
        self.y = y
        self.ylen = ylen
        self.i = pygame.image.load(img)
        self.vis = True
        object_set.append(self)

    def eaten(self, linked_counter):
        self.x = 0
        self.y = 0
        self.vis = False
        self.count += 1
        if linked_counter.value < 5:
            linked_counter.value += 1
            linked_counter.count()
        if self.ID == 10:
            newx = random.randint(30, 200)
            newy = random.randint(50, 450)
        elif self.ID == 20:
            newx = random.randint(270, 450)
            newy = random.randint(50, 450)

        if self.count < 5:
            self.renew(newx, newy)
        else:
            pass

    def show(self, disp):
        if self.vis:
            disp.blit(self.i, (self.x, self.y))

    def collide(self, *args):
        pass

    def renew(self, newx, newy):
        self.x = newx
        self.y = newy
        self.vis = True
        self.show(window)


class Counter:
    reds = {1: 'r1.png', 2: 'r2.png', 3: 'r3.png', 4: 'r4.png', 5: 'r5.png'}
    blues = {1: 'b1.png', 2: 'b2.png', 3: 'b3.png', 4: 'b4.png', 5: 'b5.png'}
    xlen = 20
    ylen = 20
    obj_type = 'counter'

    def __init__(self, x, y, object_set, color='red',  value=0,  ID=0):
        self.x = x
        self.y = y
        self.ID = ID
        self.value = value
        self.color = color
        object_set.append(self)
        self.i = pygame.image.load('r1.png')

    def count(self):
        if self.color == 'red':
            self.i = pygame.image.load(self.reds[self.value])
        else:
            self.i = pygame.image.load(self.blues[self.value])

    def show(self, disp):
        if (self.value > 0) and (self.value < 6):
            disp.blit(self.i, (self.x, self.y))

    def collide(self, *args):
        pass


pygame.init()
objects = list()
clock = pygame.time.Clock()

bg = pygame.image.load('bgGrass.jpg')
pygame.display.set_caption('яблочная лихорадка')

window = pygame.display.set_mode((500, 500))

player1 = Plr(object_set=objects, img='player.png', x=10, y=15, ID=1, direction=1)
player2 = Plr(object_set=objects, img='player1.png', x=300, y=15, ID=2, direction=2)

apple1 = Apple(100, 100, objects, ID=10)
apple2 = Apple(250, 100, objects, ID=20)

counter1 = Counter(0, 0, objects, color='red', ID=100)
counter2 = Counter(480, 0, objects, color='blue',  ID=200)


run = True
while run:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        keys = pygame.key.get_pressed()

        player1.checkmoves(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d])
        player2.checkmoves(keys[pygame.K_u], keys[pygame.K_h], keys[pygame.K_j], keys[pygame.K_k])

        window.blit(bg, (0, 0))

        for obj in objects:
            obj.show(window)
            for touched in objects:
                if checktouch(obj.x, obj.x + obj.xlen, touched.x, touched.x + touched.xlen, obj.y, obj.y + obj.ylen, touched.y, touched.y + touched.ylen):
                    obj.collide(touched, touched.obj_type)

        pygame.display.update()

pygame.quit()

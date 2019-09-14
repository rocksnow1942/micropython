from machine import Pin, I2C
import ssd1306
import time
import random

"""
jumping game
"""
# ESP8266 Pin assignment
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
button = Pin(14, Pin.IN, Pin.PULL_UP)


sun1 = [(95, 9),(96, 9),(96, 13),(97, 5),(97, 9),(97, 12),(97, 13),(98, 5),(98, 12),(99, 5),
(99, 8),(99, 9),(99, 10),(99, 11),(99, 12),(100, 7),(100, 8),(100, 9),(100, 10),(100, 11),
(100, 12),(100, 13),(100, 15),(100, 16),(101, 6),(101, 7),(101, 8),(101, 9),(101, 10),(101, 11),
(101, 12),(101, 13),(101, 14),(102, 5),(102, 6),(102, 7),(102, 8),(102, 10),(102, 12),(102, 13),
(102, 14),(102, 15),(103, 5),(103, 6),(103, 7),(103, 8),(103, 9),(103, 10),(103, 11),(103, 13),
(103, 14),(103, 15),(104, 2),(104, 3),(104, 5),(104, 6),(104, 7),(104, 8),(104, 9),(104, 10),
(104, 11),(104, 13),(104, 14),(104, 15),(104, 16),(104, 17),(104, 18),(105, 5),(105, 6),(105, 7),
(105, 8),(105, 9),(105, 10),(105, 11),(105, 13),(105, 14),(105, 15),(106, 5),(106, 6),(106, 7),
(106, 8),(106, 10),(106, 12),(106, 13),(106, 14),(106, 15),(107, 6),(107, 7),(107, 8),(107, 9),
(107, 10),(107, 11),(107, 12),(107, 13),(107, 14),(108, 4),(108, 5),(108, 7),(108, 8),(108, 9),
(108, 10),(108, 11),(108, 12),(108, 13),(108, 15),(109, 3),(109, 4),(109, 8),(109, 9),(109, 10),
(109, 11),(109, 12),(109, 16),(109, 17),(110, 17),(111, 8),(111, 12),(112, 7),(112, 8),(112, 12),
(113, 7),(113, 12),]
sun2 = [
(92, 9),(93, 9),(93, 14),(94, 9),(94, 14),(95, 9),(95, 13),(95, 14),(96, 1),(96, 2),
(96, 9),(96, 13),(97, 2),(97, 3),(97, 4),(97, 9),(97, 12),(97, 13),(98, 4),(98, 5),
(98, 12),(98, 19),(99, 5),(99, 6),(99, 8),(99, 9),(99, 10),(99, 11),(99, 12),(99, 18),
(99, 19),(100, 7),(100, 8),(100, 9),(100, 10),(100, 11),(100, 12),(100, 13),(100, 15),(100, 16),
(100, 17),(100, 18),(101, 6),(101, 7),(101, 8),(101, 9),(101, 10),(101, 11),(101, 12),(101, 13),
(101, 14),(102, 5),(102, 6),(102, 7),(102, 10),(102, 11),(102, 13),(102, 14),(102, 15),(103, 5),
(103, 6),(103, 7),(103, 9),(103, 10),(103, 11),(103, 14),(103, 15),(104, 0),(104, 1),(104, 2),
(104, 3),(104, 5),(104, 6),(104, 7),(104, 8),(104, 9),(104, 10),(104, 11),(104, 12),(104, 14),
(104, 15),(104, 16),(104, 17),(104, 18),(104, 19),(104, 20),(105, 5),(105, 6),(105, 7),(105, 8),
(105, 9),(105, 10),(105, 11),(105, 12),(105, 14),(105, 15),(106, 5),(106, 6),(106, 7),(106, 10),
(106, 11),(106, 14),(106, 15),(107, 6),(107, 7),(107, 9),(107, 10),(107, 13),(107, 14),(108, 4),
(108, 5),(108, 7),(108, 8),(108, 9),(108, 10),(108, 11),(108, 12),(108, 13),(108, 15),(108, 16),
(108, 17),(109, 3),(109, 4),(109, 8),(109, 9),(109, 10),(109, 11),(109, 12),(109, 16),(109, 17),
(109, 18),(110, 1),(110, 2),(110, 3),(110, 17),(110, 19),(111, 1),(111, 8),(111, 12),(111, 19),
(112, 7),(112, 8),(112, 11),(112, 12),(112, 19),(113, 7),(113, 11),(113, 12),(114, 7),(114, 11),
(115, 7),(115, 11),(116, 6),(116, 7),(116, 11),(117, 6),(117, 11),]


class Dragon():
    """
    control and draw the jumping guy
    """
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.in_air = 0
        self.max_hight = 32
        self.inairframe = 24

    def _draw(self):
        dragon = [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (1, 4), (1, 5), (1, 6), (1, 10), (1, 11),
                  (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2,
                                                           5), (2, 6), (2, 8), (2, 9), (2, 10),
                  (2, 11), (2, 14), (3, 0), (3, 1), (3, 3), (3,
                                                             4), (3, 6), (3, 8), (3, 10), (3, 11),
                  (3, 12), (3, 13), (3, 14), (4, 0), (4,
                                                      1), (4, 4), (4, 6), (4, 7), (4, 8), (4, 9),
                  (4, 10), (4, 11), (4, 14), (5, 0), (5,
                                                      1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7),
                  (5, 8), (5, 9), (5, 10), (5, 11), (6,
                                                     0), (6, 1), (6, 3), (6, 4), (6, 6), (6, 8),
                  (6, 10), (6, 11), (6, 12), (7, 1), (7,
                                                      4), (7, 6), (7, 8), (7, 9), (7, 10), (7, 12),
                  (7, 13), (7, 14), (8, 1), (8, 2), (8, 3), (8, 4), (8, 6), (8, 10), (8, 14), (9, 10), ]
        p = abs(self.in_air - self.inairframe/2)
        n = 4
        if p < self.inairframe/n:
            height_modifier = 1
        else:
            height_modifier = 1 - (p-self.inairframe/n) / \
                (1/2*self.inairframe-self.inairframe/n)

        y = self.y - self.max_hight*(height_modifier)
        for i, j in dragon:
            oled.pixel(i+self.x, int(y)+j, 1)
        return y+14

    def jump(self):
        if not self.in_air:
            self.in_air = 1

    def frame(self):
        if self.in_air and (self.in_air < self.inairframe):
            self.in_air += 1
        else:
            self.in_air = 0
        return self._draw()


class Map():
    """
    draw map
    """
    def __init__(self, stand):
        self.trees = []
        self.stand = stand
        self.maxtree = 1
        self.frequency = 1
        self.maxtreeheight = 20
        self.speed = 2
        self.road = [(random.getrandbits(3),random.getrandbits(2)) for i in range(128)]
        self.roadoffset = 0
    def _draw(self):
        score = 0
        top = 64
        for i in range(128):
            oled.pixel(i, 63, 1)
        for k,(j,h) in enumerate(self.road[self.roadoffset:]+self.road[0:self.roadoffset]):
            if not j:
                for l in range(h+1):
                    oled.pixel(k,62-l,1)
        self.roadoffset += self.speed
        if self.roadoffset >128:
            self.roadoffset-=128
        if self.roadoffset//10%2:
            sun = sun1
        else:
            sun=sun2
        for i,j in sun:
            oled.pixel(i-10,j+16,1)

        for tree in self.trees:
            self.drawtree(*tree)
            if self.stand-self.speed < tree[0] < self.stand+self.speed:
                top = 62 - tree[1]
                if (self.stand-tree[0]) in range(self.speed):
                    score = int(tree[1]/self.maxtreeheight*10)
            tree[0] -= self.speed
        if self.trees and self.trees[0][0] < -5:
            self.trees.pop(0)

        return top, score

    def drawtree(self, x, h):
        for y in range(62-h, 72-h):
            width = int((y+h-60)/2)
            xmin = x-width
            xmax = x+width
            for i in range(xmin, xmax+1):
                oled.pixel(i, y, 1)
        for y in range(72-h, 63):
            for i in range(x-1, x+2):
                oled.pixel(i, y, 1)

    def frame(self):
        seed = random.getrandbits(5)
        if seed < self.frequency and len(self.trees) < self.maxtree:
            hight = random.getrandbits(5)
            self.trees.append(
                [134, int(11 + hight/32*(self.maxtreeheight-11))])
        return self._draw()


def monitorbutton(ms):
    clicked = 0
    for i in range(int(ms)):
        time.sleep_ms(1)
        if not button.value():
            clicked = 1
    return clicked


def drawscore(score, maxscore):
    oled.text("You:{:>3} Max:{:>3}".format(
        int(score), int(maxscore)), 3, 4)


restartcount = 3
buttonclicked = False
dragon = Dragon(12, 48)
treemap = Map(12)
score = 0
maxscore = 0
gameover = False


def drawgameover():
    global restartcount, gameover, score, maxscore, dragon, treemap, buttonclicked
    oled.text("Game Over!!", 5, 4)
    oled.text("Your Score:{:>3}".format(
        int(score), ), 5, 20)
    if int(score) > int(maxscore):
        oled.text("New Best Score!", 5, 30)
    if restartcount:
        restartcount -= 1
        oled.text("Restart in {}...".format(restartcount), 2, 40)
    else:
        if buttonclicked:
            gameover = False
            maxscore = max(score, maxscore)
            score = 0
            restartcount = 3
            dragon = Dragon(12, 48)
            treemap = Map(12)
        else:
            oled.text("Click Button", 15, 40)
            oled.text("To Continue ...", 10, 50)
    buttonclicked = monitorbutton(900)

while True:
    oled.fill(0)
    if not gameover:
        if buttonclicked:
            dragon.jump()
        dragonbutt = dragon.frame()
        treetop, s = treemap.frame()
        score += s + 0.15*treemap.speed
        treemap.maxtree = min(1+score//150,9)
        treemap.frequency = min(1 + score//150,10)
        treemap.speed = min(2+ int(score//300),9)
        drawscore(score, maxscore)
        if treetop < dragonbutt:
            gameover = True
            continue
        buttonclicked = monitorbutton(10)
    else:
        drawgameover()
    oled.show()

from machine import Pin, I2C
import ssd1306
from time import sleep
import random
import utime
import network
import config
from ntptime import settime
"""
this script generate a time and random hearts
"""
# ESP8266 Pin assignment
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

button = Pin(14, Pin.IN, Pin.PULL_UP)

def connect_wifi():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():

        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            sleep(1)


def draw_header(hit,total):
    oled.text('Accuracy: {:.1f}% Total Fire: {}, Hit: {}'.format(hit/total*100, total, hit),0,0)


def draw_heart(x,y,color=1):
    heart =[(0, 2),(0, 3),(0, 4),(0, 5),(0, 6),(0, 7),(1, 2),(1, 3),(1, 4),(1, 5),(1, 6),(1, 7),(2, 0),
            (2, 1),(2, 2),(2, 3),(2, 4),(2, 5),(2, 6),(2, 7),(2, 8),(2, 9),(3, 0),(3, 1),(3, 2),(3, 3),
            (3, 4),(3, 5),(3, 6),(3, 7),(3, 8),(3, 9),(4, 0),(4, 1),(4, 2),(4, 3),(4, 4),(4, 5),(4, 6),
            (4, 7),(4, 8),(4, 9),(4, 10),(4, 11),(5, 0),(5, 1),(5, 2),(5, 3),(5, 4),(5, 5),(5, 6),(5, 7),
            (5, 8),(5, 9),(5, 10),(5, 11),(6, 2),(6, 3),(6, 4),(6, 5),(6, 6),(6, 7),(6, 8),(6, 9),(6, 10),
            (6, 11),(6, 12),(6, 13),(7, 2),(7, 3),(7, 4),(7, 5),(7, 6),(7, 7),(7, 8),(7, 9),(7, 10),(7, 11),
            (7, 12),(7, 13),(8, 0),(8, 1),(8, 2),(8, 3),(8, 4),(8, 5),(8, 6),(8, 7),(8, 8),(8, 9),(8, 10),
            (8, 11),(9, 0),(9, 1),(9, 2),(9, 5),(9, 6),(9, 7),(9, 8),(9, 9),(9, 10),(9, 11),(10, 0),(10, 1),
            (10, 2),(10, 5),(10, 6),(10, 7),(10, 8),(10, 9),(11, 0),(11, 1),(11, 2),(11, 3),(11, 4),(11, 5),(11, 6),
            (11, 7),(11, 8),(11, 9),(12, 2),(12, 3),(12, 4),(12, 5),(12, 6),(12, 7),(13, 2),(13, 3),(13, 4),(13, 5),
            (13, 6),(13, 7)]
    for i,j in heart:
        oled.pixel(i+x,j+y,color)

def monitorbutton(second):
   for i in range(int(second/0.002)):
       sleep(0.002)
       if not button.value():
           return 1
   return 0

def draw_time(x,y):
    r = utime.localtime(utime.mktime(utime.localtime()) - 7*3600)
    day=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    oled.text("{:>2}:{:>2}:{:>2} {}".format(r[3],r[4],r[5],day[r[6]]),x,y)


connect_wifi()
settime()


hearts = [[60,40],[30,40],[90,40]]

while True:
    oled.fill(0)
    trigger = monitorbutton(0.1)

    if trigger:
        hearts = [[60,40],[30,40],[90,40]]
        modifier = 3
    else:
        modifier = 1
    for i in range(3):
        pos_x,pos_y= hearts[i]
        randomx=random.getrandbits(1)
        randomy=random.getrandbits(1)
        pos_x+= (randomx or -1) * modifier
        pos_y+= (randomy or -1) * modifier
        pos_x = min(115,max(0,pos_x))
        pos_y = min(52,max(17,pos_y))
        hearts[i]=[pos_x,pos_y]
    draw_heart(0,0,1)
    for x,y in hearts:
        draw_heart(x,y,1)
    draw_time(17,4)
    oled.show()


a=[1,2,3]
print(a[0:3])

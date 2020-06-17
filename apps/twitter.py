import network
import time
import urequests
import config
import machine


led = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)


def connect_wifi():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())

def call_webhook(content):
    print('Invoking webhook')
    _ = urequests.post(config.TWITTER_URL,
                             json={'value1': content})



ledstatus = 1
onoff = False
def monitorbutton(second):
   for i in range(int(second/0.05)):
       time.sleep(0.1)
       if not button.value():
           return 1
   return 0


def flash():
   global ledstatus
   if onoff:
       if ledstatus:
           led.on()
           led2.off()
           ledstatus = 0
       else:
           led.off()
           led2.on()
           ledstatus = 1
   else:
       pass


connect_wifi()

while True:
   flash()
   trigger = monitorbutton(0.2)
   if trigger:
       onoff = not onoff
       if not onoff:
           led2.on()
           led.on()
       content = "lights {}".format('on' if onoff else 'off')
       call_webhook(content)
       time.sleep(0.2)

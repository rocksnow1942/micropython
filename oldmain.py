from machine import Pin,PWM,I2C,ADC
import utime
import ssd1306
from pressure import Pressure
#TODO
# use Pin 13 as the other side of measure. so that can alternate measure.

class Controller:
    def __init__(self,btnGap=200,):
        self.btnGap = btnGap

        i2c = I2C(scl=Pin(5),sda=Pin(4))
        
        self.d = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.p = Pressure(i2c)
        
        self.pwm = PWM(Pin(13))
        self.pwm.duty(0)
        self.pwm.freq(90) # pwm duty 19 - 134
        self.button = Pin(12, Pin.IN,Pin.PULL_UP)

        self.led = Pin(2,Pin.OUT)
        self.led.on() # this turn on board led off

        self.adc = ADC(0)
        self.pwr = Pin(14, Pin.OUT,)
        self.pwr.off()

        self.t1 = 0 
        self.t2 = 0
        self.title = 'Liquid Monitor'

        self.pump = False
        self.speed = 0
        self.cond = 0
        self.pumpON = False
        self.initSpeed = 300
        self.btnExit = False
        self.lastCond = 0
        self.pressure=0
        self.temp=0

    def ledON(self):
        self.led.off()
    def ledOFF(self):
        self.led.on()

    def setPump(self,value):
        self.pwm.duty(int(value))
   
    def measure(self,wait=0,N=3):
        "measure method"
        res = []
        for i in range(N):
            res.append( self.singleM(wait) ) 
            utime.sleep_ms(50)
        self.cond = sum(res)//N
        # measure temperatuer and pressurre
        self.pressure,self.temp = self.p.read()

         

    def singleM(self,wait=0):
        self.pwr.on()
        utime.sleep_ms(wait)
        cond = self.adc.read()
        self.pwr.off()
        return cond

    def update(self):
        "determine if need to turn on pump"
        if self.pump:
            if self.cond >= 20:
                self.lastCond = self.cond
                self.speed -= 30
                if self.speed <= 200:
                    self.speed = 0
                self.setPump(self.speed)
            else:    
                self.speed+=10
                if self.speed<=200:
                    self.speed = 200
                self.speed = min(1024,self.speed)
                self.setPump(self.speed)
        else:
            self.setPump(0)
            self.speed = 0
            
    
   

    def show(self):
        self.d.fill(0)
        self.d.text(self.title,0,2)
        self.d.text('Cond.  :{:>6d}'.format(self.cond), 0, 20) 
        self.d.text('LastC. :{:>6d}'.format(self.lastCond),0, 31)
        self.d.text('Pump   :{:>6}'.format(self.speed if self.pump else "OFF"), 0, 42)
        self.d.text('PSI:{:>4.1f} T: {:.1f}'.format(self.pressure,self.temp),0, 53)        
        self.d.show()

    def text(self,header="", msg=""):
        self.d.fill(0)
        
        self.d.text(header, 0, 2)
        for i in range(len(msg)//16+1):
            self.d.text(msg[i*16:(i+1)*16], 0, i*10 + 16)
        self.d.show()

    def monitorButton(self):
        self.t1 = utime.ticks_ms()
        while True:
            self.t2 = utime.ticks_ms()
            if self.button.value() == 0:
                self.pump = not self.pump
                break
            if (self.t2 - self.t1 >= self.btnGap) or ((self.t2 - self.t1)<=0):
                break 
        while (self.button.value() == 0):
            self.ledON()
            utime.sleep_ms(50)
            self.ledOFF()
            utime.sleep_ms(50)
            if (utime.ticks_ms() - self.t1)>3000:
                self.title = "System Exited."
                self.show()
                self.btnExit = True
                raise Exception ('exit')
            

def mainLoop():
    btnExit = False
    try:
       
        control = Controller(btnGap=200,)

        while True:
            control.ledON()
            control.monitorButton()
            control.measure()
            control.update()
            control.show()
            control.ledOFF()
            utime.sleep_ms(1000)
    except Exception as e:
        if not control.btnExit:
            control.text(header='error',msg=str(e))
    finally:
        control.setPump(0)
        control.ledOFF()
        if control.btnExit:
            control.text(header="System Exited.",msg="Button Hold > 3s, system shut down. Power cycle controller to restart.")

mainLoop()


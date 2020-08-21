from machine import Pin,PWM,I2C
import utime
import ssd1306
from pid import PID

trig=Pin(15, Pin.OUT)
echo=Pin(13, Pin.IN)
pwm = PWM(Pin(12))
pwm.freq(50) # pwm duty 19 - 134
button = Pin(0, Pin.IN, Pin.PULL_UP)



class Controller:
    def __init__(self,btnGap=200):
        self.btnGap = btnGap
        i2c = I2C(scl=Pin(5),sda=Pin(4))
        self.d = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.waterLevel = 0 
        self.setLevel = 100 
        self.pump = 0
        self.pid = PID(Kp=10,Ki=1,Kd=1,
                       setpoint=self.setLevel,
                       output_limits=(19,134))
        self.clicked = False
        self.t1 = 0 
        self.t2 = 0

    def setPump(self,value):
        pwm.duty(int(value))

    def update(self, ):
        self.getDistance()
        if self.clicked:
            self.setLevel = self.waterLevel

        self.pid.setpoint = self.setLevel

        self.pump = 153 - self.pid(self.waterLevel)
        self.setPump( self.pump )
        
        

    def show(self):
        self.d.fill(0)
        self.d.text('Liquid Monitor',0,2)
        self.d.text('Current:{:>6.1f}cm'.format(self.waterLevel), 0, 20) 
        self.d.text('Set    :{:>6.1f}cm'.format(self.setLevel), 0, 37)
        self.d.text('Pump   :{:>6.1f}'.format(self.pump),0, 54)
        self.d.show()

    def text(self,header=None, msg=None):
        self.display.fill(0)
        
        self.display.text(self.header, 0, 2)
        for i in range(len(self.msg)//16+1):
            self.display.text(self.msg[i*16:(i+1)*16], 0, i*10 + 16)
        self.display.show()

    def getDistance(self):
        trig.off()
        utime.sleep_us(2)
        trig.on()
        utime.sleep_us(10)
        trig.off()
        while echo.value() == 0:
            pass
        self.t1 = utime.ticks_us()
        while echo.value() == 1:
            pass
        self.t2 = utime.ticks_us()
        self.waterLevel = (self.t2 - self.t1) / 58.0

    def monitorButton(self):
        self.t1 = utime.ticks_ms()
        while True:
            self.t2 = utime.ticks_ms()
            if not button.value():
                self.clicked = True
                break
            if (self.t2 - self.t1 >= self.btnGap) or ((self.t2 - self.t1)<=0):
                self.clicked = False
                break 
        
        
 
    
  




def mainLoop():
    control = Controller(btnGap=200)

    while True:
        control.monitorButton()
        control.update()
        control.show()
        utime.sleep_ms(200)


mainLoop()


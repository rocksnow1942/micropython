from machine import Pin,PWM,I2C,UART
import utime
import ssd1306
from pid import PID
from us100 import US100UART
import uos

pwm = PWM(Pin(12))
pwm.freq(90) # pwm duty 19 - 134
button = Pin(0, Pin.IN, Pin.PULL_UP)





class Controller:
    def __init__(self,btnGap=200,uart=None):
        self.btnGap = btnGap
        self.uart=uart
        i2c = I2C(scl=Pin(5),sda=Pin(4))
        self.d = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.waterLevel = 0 
        self.setLevel = 100 
        self.pump = 0
        self.pid = PID(Kp=10,Ki=1,Kd=1,
                       setpoint=self.setLevel,
                       output_limits=(0,100))
        self.clicked = False
        self.t1 = 0 
        self.t2 = 0
        self.title = 'Liquid Monitor'
        self.temperature = 0

    def setPump(self,value):
        pwm.duty(int(value))

    def update(self, ):
        self.getDistance()
        if self.clicked:
            self.setLevel = self.waterLevel

        self.pid.setpoint = self.setLevel
        
        self.pump =  100 - self.pid(self.waterLevel)
        
        # if water Level is too weird, turn off the pump.
        if  self.waterLevel>200:
            self.pump = 0
        
        self.setPump( self.pump * 10.24 if self.pump >19.53 else 0 )
        
        

    def show(self):
        self.d.fill(0)
        self.d.text(self.title,0,2)
        self.d.text('Current:{:>6.1f}mm'.format(self.waterLevel), 0, 20) 
        self.d.text('Set    :{:>6.1f}mm'.format(self.setLevel), 0, 31)
        self.d.text('Pump   :{:>6.1f}'.format(self.pump),0, 42)
        self.d.text('Temp   :{:>6.1f}dC'.format(self.temperature),0, 53)
        self.d.show()

    def text(self,header=None, msg=None):
        self.display.fill(0)
        
        self.display.text(self.header, 0, 2)
        for i in range(len(self.msg)//16+1):
            self.display.text(self.msg[i*16:(i+1)*16], 0, i*10 + 16)
        self.display.show()

    def getDistance(self):
        self.waterLevel = self.uart.distance()
        self.temperature = self.uart.temperature()
        

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
        while (not button.value()):
            utime.sleep_us(10)
        if (utime.ticks_ms() - self.t1)>2000:
            self.title = "Exit System"
            self.show()
            raise Exception ('exit')

def mainLoop():
    try:
        uos.dupterm(None, 1)  # disable REPL on UART(0)
        
        control = Controller(btnGap=200,uart=US100UART(UART(0)))

        while True:
            control.monitorButton()
            control.update()
            control.show()
            utime.sleep_ms(200)
    except Exception as e:
        print(e)
    finally:
        uos.dupterm(UART(0, 115200), 1)
        
    


mainLoop()


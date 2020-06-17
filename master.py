import uos
import machine
import ssd1306
import sys
import time
from machine import UART
import random
# button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
i2c = machine.I2C(scl=machine.Pin(5),
                  sda=machine.Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


def main():
    try:
        uos.dupterm(None, 1)  # disable REPL on UART(0)
        uart = machine.UART(0)
        uart.init(230400, timeout=3000, bits=8, parity=None, stop=1, rxbuf=128)
        while True:
            time.sleep(3)
            start = random.getrandbits(4)
            bits = random.getrandbits(2)+1
            tosend = 'abcdefghijklmopqrstuvwxyz'[start:start+bits]
            uart.write('e\nsend_string "{}"\n\n'.format(tosend))
            display.fill(0)
            display.text('S:{}'.format(tosend), 0, 16)
            display.show()

            time.sleep(3)

            if uart.any():
                hostMsg = uart.read()
                if hostMsg is not None:
                    strMsg = hostMsg.decode().strip('\r\n')

                    display.fill(0)
                    display.text('R:{}'.format(strMsg), 0, 16)
                    display.show()
                    
                    if strMsg.startswith('\x03'):
                        raise Exception('Cto repl')
                    elif strMsg.startswith('\x00'):
                        raise Exception('STOP code')
                    else:
                        pass 
                        # uart.write(('Back to you. ' + strMsg + '\r\n'))
    except Exception as err:
        uart.write('Exception was raised')
        display.fill(0)
        display.text('{}'.format(err), 0, 16)
        display.show()
    finally:
        uos.dupterm(machine.UART(0, 115200), 1)


# Run main loop
main()


#   cp ./main.py /pyboard


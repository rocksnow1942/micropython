import machine
import uos
import time
led = machine.Pin(2, machine.Pin.OUT)
led.on()

def main():
    try:
        uos.dupterm(None, 1)  # disable REPL on UART(0)
        uart = machine.UART(0)
        uart.init(115200, timeout=3000, bits=8, parity=None, stop=1, rxbuf=128)
        while True:
            if uart.any():
                hostMsg = uart.readline()
                
                if hostMsg is not None:
                    strMsg = hostMsg.decode().strip('\r\n')
                    if '\x03' in strMsg:
                        raise Exception('Cto repl')
                    elif strMsg == '\x00':
                        raise Exception('STOP code')
                    else:
                        for i in range(len(strMsg)):
                            led.off()
                            time.sleep(0.05)
                            led.on()
                            time.sleep(0.1)
                        uart.write(strMsg+'\n')
                        
    except Exception as err:
        uart.write('Exception was raised')
        led.on()        
        
    finally:
        uos.dupterm(machine.UART(0, 115200), 1)

# Run main loop
main()


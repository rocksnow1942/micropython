import uos
import machine
import time

def read_response(uart,timeout=15000):
    starttime = time.ticks_ms()
    nonecount = 0
    while True:
        if nonecount>=2:
            break
        # if time.ticks_ms() - starttime >= timeout:
        #     yield 'Read time out.'
        #     break
        response = uart.readline()
        if response==None:
            nonecount += 1
            continue
        str_line = response.decode('ascii')
        yield str_line
       
        
            

def talktopico(msg,timeout=5000):
    try:
        uos.dupterm(None, 1)  # disable REPL on UART(0)
        uart = machine.UART(0)
        uart.init(230400, timeout=3000, bits=8, parity=None, stop=1, rxbuf=128*16)
        uart.write('\n\n')
        # while uart.any():
        uart.read()
        uart.write(msg)
        yield from read_response(uart)
    except Exception as err:
        yield str(err)
    finally:
        uos.dupterm(machine.UART(0, 115200), 1)

   

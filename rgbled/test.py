from tlc import TLC59711

class SPI:
    def __init__(self):
        self.wh = []
    def write(self,x):
        self.wh.append(x)
        print(f'write SPI: {x}')
        
        
t = TLC59711(SPI())


t[1] = (65535,65535,65535)


t.show()



bytearray(b'\x96\xdf\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
b'\x96\xdf\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

b'\x96\xdf\xff\xff\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


class Pressure:
    "for SSCMANN060PG2A3 pressure sensor"
    def __init__(self,i2c,addr=40):
        self.addr=addr
        self.i2c = i2c
        self.buf = bytearray(3)
    
    def read(self):
        "return Pressure and temperature"
        self.i2c.readfrom_into(self.addr, self.buf)
        if self.buf[0]>>6:
            return 0,0
        return (( self.buf[0] * 256 + self.buf[1] - 1638) * 60 / (14745-1638) , # pressure
        (self.buf[2]<<3) / 2047 * 200 - 50) # temperature
        

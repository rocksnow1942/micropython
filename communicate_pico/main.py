from ws_server import WebSocketServer, WebSocketClient
from ws_connection import ClientClosedError
import uos
import machine
import ssd1306
import network
import time
from pico_commu import talktopico



class Display:
    def __init__(self):
        i2c = machine.I2C(scl=machine.Pin(5),
                          sda=machine.Pin(4))
        self.display = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.header = 'ESP8266'
        self.msg = "Welcome To ESP8266 Board!"

    def text(self,header=None, msg=None):
        self.display.fill(0)
        self.header = header if header!=None else self.header
        self.msg = msg if msg!=None else self.msg
        self.display.text(self.header, 0, 2)
        for i in range(len(self.msg)//16+1):
            self.display.text(self.msg[i*16:(i+1)*16], 0, i*10 + 16)
        self.display.show()


display = Display()


class TestClient(WebSocketClient):
    def __init__(self, conn):
        super().__init__(conn)
        adr = conn.address 
        display.text(msg='connected to: '+adr[0])
        
    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8").replace('\\n', '\n').replace('\\t','\t')
            
            # print(repr(msg))
            display.text(msg="received:" + msg)
            for response in talktopico(msg):
                self.connection.write(repr(response))
        except ClientClosedError:
            print('error close')
            self.connection.close()




class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__("test.html", 2)

    def _make_client(self, conn):
        return TestClient(conn)

server = TestServer()
server.start()
try:
    while True:
        server.process_all()
        display.text(header='Clients: '+str(len(server._clients))) 
        if len(server._clients) == 0:
            for i in (network.AP_IF, network.STA_IF):
                iface = network.WLAN(i)
                if iface.active():
                    ipaddress = iface.ifconfig()[0]
            display.text(msg='Web server at: '+ipaddress)
except KeyboardInterrupt:
    pass
server.stop()



#   cp ./main.py /pyboard




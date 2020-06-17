import dht
import framebuf
import machine
import ssd1306
import sys
import time






def get_temperature_and_humidity():
    dht22 = dht.DHT22(machine.Pin(12))
    dht22.measure()
    temperature = dht22.temperature()
    return temperature, dht22.humidity()



def display_temperature_and_humidity(temperature, humidity):
    i2c = machine.I2C(scl=machine.Pin(5),
                      sda=machine.Pin(4))
   
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.fill(0)

    display.text('{:^16s}'.format('Temperature:'), 0, 0)
    display.text('{:^16s}'.format(str(temperature) +
                                  ('F' if config.FAHRENHEIT else 'C')), 0, 16)

    display.text('{:^16s}'.format('Humidity:'), 0, 32)
    display.text('{:^16s}'.format(str(humidity) + '%'), 0, 48)

    display.show()
    time.sleep(10)
    display.poweroff()


button = Pin(14, Pin.IN, Pin.PULL_UP)

def run():
    while True:
        time.sleep_ms(10)
        if not button.value():
            temperature, humidity = get_temperature_and_humidity()
            display_temperature_and_humidity(temperature, humidity)
    

run()

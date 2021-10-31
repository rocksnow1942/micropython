from machine import SPI

spi = SPI(1, baudrate=1000000, polarity=0, phase=0)
from tlc import TLC



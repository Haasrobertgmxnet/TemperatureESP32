# bme280.py 
# 
from machine import I2C
import time

class BME280:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr
        # Init-Befehl hier, wenn nötig
    def read_compensated_data(self):
        # Hier müsstest du den echten Sensor-Code haben,
        # der Temperatur, Feuchte und Druck liest und kompensiert.
        # Für den Zweck nehmen wir Dummywerte:
        temp = 25.0
        pres = 1013.25
        hum = 40.0
        return temp, pres, hum
    @property
    def temperature(self):
        return self.read_compensated_data()[0]
    @property
    def pressure(self):
        return self.read_compensated_data()[1]
    @property
    def humidity(self):
        return self.read_compensated_data()[2]

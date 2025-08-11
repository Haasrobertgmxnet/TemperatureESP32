# TMP117 Treiber als kleine Klasse
class TMP117:
    def __init__(self, i2c, addr=0x48):
        self.i2c = i2c
        self.addr = addr
        # Konfigurationsregister (optional): Normalbetrieb
        # self.i2c.writeto_mem(self.addr, 0x01, b'\x02\x00')  # z.B. shutdown deaktivieren
    def read_temp(self):
        # Temperaturregister ist 0x00, 16-bit
        data = self.i2c.readfrom_mem(self.addr, 0x00, 2)
        raw = data[0] << 8 | data[1]
        # TMP117 gibt Temperatur in 0.0078125 Grad pro LSB
        if raw & 0x8000:  # negativ
            raw -= 1 << 16
        temp_c = raw * 0.0078125
        return temp_c
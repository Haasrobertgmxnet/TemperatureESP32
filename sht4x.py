import time

class SHT4x:
    DEFAULT_ADDR = 0x44

    def __init__(self, i2c, address=DEFAULT_ADDR):
        self.i2c = i2c
        self.addr = address

    def _send_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytes([cmd]))

    @property
    def measurements(self):
        # Single shot high precision measurement command
        self._send_cmd(0xFD)
        time.sleep(0.01)
        data = self.i2c.readfrom(self.addr, 6)
        temp_raw = data[0] << 8 | data[1]
        rh_raw   = data[3] << 8 | data[4]
        temp_c = -45 + (175 * (temp_raw / 65535.0))
        rh = 100 * (rh_raw / 65535.0)
        return temp_c, rh


# bmp280.py – funktionierende MicroPython-Version
import time
from micropython import const

# Register-Adressen
_CHIP_ID = const(0xD0)
_RESET = const(0xE0)
_CTRL_MEAS = const(0xF4)
_CONFIG = const(0xF5)
_PRESSURE_DATA = const(0xF7)
_TEMP_DATA = const(0xFA)

class BMP280:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr

        # Check chip ID
        if self.i2c.readfrom_mem(self.addr, _CHIP_ID, 1)[0] != 0x58:
            raise OSError("BMP280 not found")

        self._read_calibration()
        self._write_reg(_CTRL_MEAS, 0x27)
        self._write_reg(_CONFIG, 0xA0)

    def _read_calibration(self):
        calib = self.i2c.readfrom_mem(self.addr, 0x88, 24)
        self.dig_T1 = calib[1] << 8 | calib[0]
        self.dig_T2 = self._signed(calib[3] << 8 | calib[2])
        self.dig_T3 = self._signed(calib[5] << 8 | calib[4])
        self.dig_P1 = calib[7] << 8 | calib[6]
        self.dig_P2 = self._signed(calib[9] << 8 | calib[8])
        self.dig_P3 = self._signed(calib[11] << 8 | calib[10])
        self.dig_P4 = self._signed(calib[13] << 8 | calib[12])
        self.dig_P5 = self._signed(calib[15] << 8 | calib[14])
        self.dig_P6 = self._signed(calib[17] << 8 | calib[16])
        self.dig_P7 = self._signed(calib[19] << 8 | calib[18])
        self.dig_P8 = self._signed(calib[21] << 8 | calib[20])
        self.dig_P9 = self._signed(calib[23] << 8 | calib[22])

    def _write_reg(self, reg, data):
        self.i2c.writeto_mem(self.addr, reg, bytes([data]))

    def _read_raw_data(self):
        data = self.i2c.readfrom_mem(self.addr, _PRESSURE_DATA, 6)
        adc_P = data[0] << 12 | data[1] << 4 | (data[2] >> 4)
        adc_T = data[3] << 12 | data[4] << 4 | (data[5] >> 4)
        return adc_T, adc_P

    def _signed(self, val):
        return val - 65536 if val > 32767 else val

    @property
    def temperature(self):
        adc_T, _ = self._read_raw_data()
        var1 = (((adc_T >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((adc_T >> 4) - self.dig_T1) * ((adc_T >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        self.t_fine = var1 + var2
        T = (self.t_fine * 5 + 128) >> 8
        return T / 100.0

    @property
    def pressure(self):
        _, adc_P = self._read_raw_data()
        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33
        if var1 == 0:
            return 0
        p = 1048576 - adc_P
        p = ((p << 31) - var2) * 3125 // var1
        var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.dig_P8 * p) >> 19
        p = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)
        return p / 25600.0


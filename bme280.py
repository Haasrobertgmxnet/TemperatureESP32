import time
# from machine import I2C

# BME280_I2CADDR = 0x76

class BME280:
    def __init__(self, i2c, address=0x76):
        print("Inside __init__")
        self.i2c = i2c
        self.address = address

        # Chip-ID prüfen (0x60 = BME280)
        chip_id = self._read_byte(0xD0)
        if chip_id != 0x60:
            raise RuntimeError("Kein BME280 gefunden, Chip-ID: 0x{:02x}".format(chip_id))

        # Reset
        self._write_byte(0xE0, 0xB6)
        time.sleep_ms(300)

        # Kalibrationsdaten einlesen
        self._load_calibration_data()

        # Humidity oversampling einstellen
        self._write_byte(0xF2, 0x01)
        # ctrl_meas: temp & pressure oversampling x1, normal mode
        self._write_byte(0xF4, 0x27)
        # config: standby 0.5ms, filter off
        self._write_byte(0xF5, 0xA0)

    # --- Low-Level I²C ---
    def _read_byte(self, register):
        return int.from_bytes(self.i2c.readfrom_mem(self.address, register, 1), 'little')

    def _read_bytes(self, register, length):
        return self.i2c.readfrom_mem(self.address, register, length)

    def _write_byte(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytes([value]))

    # --- Kalibration ---
    def _load_calibration_data(self):
        # Temp & Pressure
        calib = self._read_bytes(0x88, 24)
        self.dig_T1 = int.from_bytes(calib[0:2], 'little')
        self.dig_T2 = int.from_bytes(calib[2:4], 'little', signed=True)
        self.dig_T3 = int.from_bytes(calib[4:6], 'little', signed=True)

        self.dig_P1 = int.from_bytes(calib[6:8], 'little')
        self.dig_P2 = int.from_bytes(calib[8:10], 'little', signed=True)
        self.dig_P3 = int.from_bytes(calib[10:12], 'little', signed=True)
        self.dig_P4 = int.from_bytes(calib[12:14], 'little', signed=True)
        self.dig_P5 = int.from_bytes(calib[14:16], 'little', signed=True)
        self.dig_P6 = int.from_bytes(calib[16:18], 'little', signed=True)
        self.dig_P7 = int.from_bytes(calib[18:20], 'little', signed=True)
        self.dig_P8 = int.from_bytes(calib[20:22], 'little', signed=True)
        self.dig_P9 = int.from_bytes(calib[22:24], 'little', signed=True)

        # Humidity
        self.dig_H1 = self._read_byte(0xA1)
        calib_h = self._read_bytes(0xE1, 7)
        self.dig_H2 = int.from_bytes(calib_h[0:2], 'little', signed=True)
        self.dig_H3 = calib_h[2]
        e4 = calib_h[3]
        e5 = calib_h[4]
        e6 = calib_h[5]
        self.dig_H4 = (e4 << 4) | (e5 & 0x0F)
        if self.dig_H4 & 0x800:  # sign extension
            self.dig_H4 -= 1 << 12
        self.dig_H5 = (e6 << 4) | (e5 >> 4)
        if self.dig_H5 & 0x800:
            self.dig_H5 -= 1 << 12
        self.dig_H6 = calib_h[6]
        if self.dig_H6 & 0x80:
            self.dig_H6 -= 256

    # --- Rohdaten ---
    def _read_raw_data(self):
        data = self._read_bytes(0xF7, 8)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        adc_h = (data[6] << 8) | data[7]
        return adc_t, adc_p, adc_h

    # --- Messungen ---
    def read_compensated_data(self):
        adc_t, adc_p, adc_h = self._read_raw_data()

        # Temperatur
        var1 = (((adc_t >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((adc_t >> 4) - self.dig_T1) * ((adc_t >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        t_fine = var1 + var2
        temperature = (t_fine * 5 + 128) >> 8
        temperature = temperature / 100.0

        # Druck
        var1 = t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33
        if var1 == 0:
            pressure = 0
        else:
            p = 1048576 - adc_p
            p = (((p << 31) - var2) * 3125) // var1
            var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (self.dig_P8 * p) >> 19
            pressure = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)
            pressure = pressure / 256.0 / 100.0  # in hPa

        # Feuchtigkeit
        h = t_fine - 76800
        h = (((((adc_h << 14) - (self.dig_H4 << 20) - (self.dig_H5 * h)) + 16384) >> 15) * (((((((h * self.dig_H6) >> 10) * (((h * self.dig_H3) >> 11) + 32768)) >> 10) + 2097152) * self.dig_H2 + 8192) >> 14))
        h = h - (((((h >> 15) * (h >> 15)) >> 7) * self.dig_H1) >> 4)
        h = max(0, min(419430400, h))
        humidity = (h >> 12) / 1024.0

        return temperature, pressure, humidity

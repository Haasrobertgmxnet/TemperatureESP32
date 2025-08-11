from machine import Pin, I2C
import network
import ntptime
import time
import ssd1306
import bmp280
import sht4x   # Treiber für SHT45
from tmp117 import TMP117  # Angenommen, TMP117-Treiber hast du als tmp117.py
from bme280 import BME280  # BME280-Treiber (MicroPython)
from config import WIFI_SSID, WIFI_PASSWORD  # Deine WLAN-Zugangsdaten

# WLAN-Verbindung herstellen
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Verbinde mit WLAN...")
        try:
            wlan.connect(ssid, password)
        except:
            print("Kein WLAN gefunden")
            return False
        for _ in range(100):
            if wlan.isconnected():
                break
            time.sleep(0.1)
    if wlan.isconnected():
        print("WLAN verbunden:", wlan.ifconfig())
        return True
    else:
        print("WLAN-Verbindung fehlgeschlagen.")
        return False

# Uhrzeit synchronisieren
def sync_time(offset_hours=2):
    try:
        ntptime.settime()
        print("Uhrzeit synchronisiert.")
        return time.time() + offset_hours * 3600
    except:
        print("Zeit konnte nicht synchronisiert werden.")
        return time.time()

do_logging = False

def main():
    # I2C einrichten
    i2c = I2C(0, scl=Pin(5), sda=Pin(4))
    print("I2C scan:", [hex(x) for x in i2c.scan()])

    has_bmp280 = has_bme280 = has_sht45 = has_tmp117 = False
    
    devices = i2c.scan()

    # Sensorerkennung
    if 0x76 in devices or 0x77 in devices:
        try:
            bme_addr = 0x76 if 0x76 in devices else 0x77
            bme = BME280(i2c=i2c, addr=bme_addr)
            has_bme280 = True
            print("BME280 gefunden an Adresse", hex(bme_addr))
        except Exception as e:
            print("BME280 initialisierung fehlgeschlagen:", e)
    elif 0x76 in devices:
        try:
            bmp = bmp280.BMP280(i2c)
            has_bmp280 = True
            print("BMP280 gefunden.")
        except Exception as e:
            print("BMP280 initialisierung fehlgeschlagen:", e)

    if 0x3C not in devices:
        raise OSError("OLED nicht gefunden.")
    else:
        print("OLED gefunden.")

    if 0x44 in devices:
        try:
            sht = sht4x.SHT4x(i2c)
            has_sht45 = True
            print("SHT45 gefunden.")
        except Exception as e:
            print("SHT45 initialisierung fehlgeschlagen:", e)

    if 0x48 in devices:
        try:
            tmp = TMP117(i2c)
            has_tmp117 = True
            print("TMP117 gefunden.")
        except Exception as e:
            print("TMP117 initialisierung fehlgeschlagen:", e)

    # OLED starten
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    rtc_offset = 2

    # WLAN verbinden und Zeit holen
    if connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        base_time = sync_time(rtc_offset)
    else:
        print("Setze fort ohne WLAN")

    if do_logging:
        # Datei vorbereiten (Header mit allen Messgrößen)
        filename = "log.csv"
        try:
            with open(filename, "x") as f:
                f.write("timestamp,temp_C,pressure_hPa,humidity_pct,sht_temp_C,sht_rh,tmp117_temp_C\n")
        except OSError:
            # Datei existiert vermutlich schon
            pass

        print("Logging gestartet. Speichere in:", filename)

    while True:
        # Messwerte lesen
        if has_bme280:
            bmp_t = bme.temperature
            bmp_p = bme.pressure
            bmp_h = bme.humidity
        elif has_bmp280:
            bmp_t = bmp.temperature
            bmp_p = bmp.pressure
            bmp_h = 0.0
        else:
            bmp_t = bmp_p = bmp_h = 0.0

        if has_sht45:
            sht_t, sht_rh = sht.measurements
        else:
            sht_t = sht_rh = 0.0

        if has_tmp117:
            tmp_t = tmp.read_temp()
        else:
            tmp_t = 0.0

        # Zeitstempel erstellen
        now = time.localtime(time.time() + rtc_offset * 3600)
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*now[:6])

        if do_logging:
            # Daten in Datei schreiben
            with open(filename, "a") as f:
                f.write("{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n".format(
                    timestamp, bmp_t, bmp_p, bmp_h, sht_t, sht_rh, tmp_t))

        # OLED anzeigen
        line_ofs = 12
        
        oled.fill(0)
        oled.text(timestamp[11:], 0, 0)  # Uhrzeit
        oled.text("Temperatures:", 0, 1*line_ofs)
        oled.text("BME: {:.1f} C".format(bmp_t), 0, 2*line_ofs)
        oled.text("TMP: {:.1f} C".format(tmp_t), 0, 3*line_ofs)
        oled.text("SHT: {:.1f} C".format(sht_t), 0, 4*line_ofs)
        oled.show()

        time.sleep(5) # Intervall in Sekunden
        
        oled.fill(0)
        oled.text("Rel Humidities:", 0, 0)
        oled.text("BME: {:.1f} %".format(bmp_h), 0, 1*line_ofs)
        oled.text("SHT: {:.1f} %".format(sht_rh), 0, 2*line_ofs)
        oled.text("Air Pressure:", 0, 3*line_ofs)
        oled.text("BME: {:.1f} hPa".format(bmp_p), 0, 4*line_ofs)
        oled.show()

        time.sleep(5) # Intervall in Sekunden

if __name__ == "__main__":
    main()

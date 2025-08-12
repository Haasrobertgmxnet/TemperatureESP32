# TemperatureESP32

![ESP32 mit Sensoren und OLED](img/IMG_20250811_140253_HDR.jpg)
![ESP32 mit Sensoren und OLED](img/IMG_20250811_142922_HDR.jpg)

## Language / Sprache / Idioma:
[🇩🇪 Deutsch](#deutsch) | [🇪🇸 Español](#espa%C3%B1ol) | [🇬🇧 English](#english) 

---
## Deutsch

### 📌 Projektübersicht
Dieses Projekt zeigt, wie ein **ESP32** mit verschiedenen Umweltsensoren Temperatur, Luftfeuchtigkeit und Luftdruck misst,  
die Werte auf einem **SSD1306 OLED** anzeigt und gleichzeitig in einer **CSV-Datei** auf dem ESP32 speichert.  

### Microcontroller-Board
- MaESP ESP32 OLED von Makerfabs
- Chip: Espressif ESP32 WROOM-32-E
- On-board-OLED 1.3"
- Bezugsquelle und weitere Spezifikationen: [Makerfabs](https://www.makerfabs.com/makepython-esp32.html?srsltid=AfmBOoo98ESGWyOQi_EoxggwQ4zqeoW0mktzH6rABH1KU28PcvKacGX1)

### 📟 Unterstützte Sensoren
- **BME280** – Temperatur, Luftfeuchtigkeit, Luftdruck  
- **BMP280** – Temperatur, Luftdruck  
- **SHT45** – Temperatur, Luftfeuchtigkeit  
- **TMP117** – hochpräziser Temperatursensor  
- **SSD1306 OLED** – Anzeige (I2C, 128x64)  

### ✨ Funktionen
- Automatische Sensorerkennung über I2C
- WLAN-Verbindung herstellen (SSID & Passwort im Code)
- Zeitsynchronisation per NTP
- CSV-Datenlogging im internen Speicher (`log.csv`)
- Abwechselnde Anzeige von Temperatur- und Feuchtigkeitswerten auf dem OLED

### 🔌 Verdrahtung (Standard im Code)
| Komponente  | Pin ESP32 | Hinweis |
|-------------|-----------|---------|
| SDA (I2C)   | GPIO4     | Anpassbar im Code |
| SCL (I2C)   | GPIO5     | Anpassbar im Code |
| VCC         | 3.3V      | Alle Sensoren |
| GND         | GND       | Alle Sensoren |

**I2C-Standardadressen:**
- BME280 / BMP280 → `0x76` oder `0x77`
- SSD1306 OLED → `0x3C`
- SHT45 → `0x44`
- TMP117 → `0x48`

### 🚀 Installation & Verwendung
1. **MicroPython auf ESP32 flashen**  
   → z. B. mit [Thonny](https://thonny.org) oder `esptool.py`
2. **Bibliotheken hochladen** (`ssd1306.py`, `bmp280.py`, `bme280.py`, `sht4x.py`, `tmp117.py`)
3. Hauptskript `main.py` auf den ESP32 kopieren
4. Lösche in `main.py` die folgende Zaile:
   ```python
   from config import WIFI_SSID, WIFI_PASSWORD  # Deine WLAN-Zugangsdaten
   ```
   Ersetze in `main.py` `WIFI_SSID` und `WIFI_PASSWORD` mit den Daten des eigenen WLAN:
   ```python
   connect_wifi(WIFI_SSID, WIFI_PASSWORD) 
   ```
   Oder ignoriere die ersten beiden Schritte in 4. und erzeuge eine neue Datei config.py mit den Variablen `WIFI_SSID` und `WIFI_PASSWORD` für die Daten des eigenen WLANs. 
5. ESP32 starten – die Messwerte erscheinen auf dem OLED und werden in `log.csv` gespeichert.

---

## Español

### 📌 Descripción del Proyecto
Este proyecto muestra cómo un **ESP32** puede medir temperatura, humedad y presión atmosférica usando varios sensores ambientales,  
mostrar los datos en una pantalla **SSD1306 OLED** y guardarlos en un **archivo CSV** en el ESP32.  

### Placa de microcontrolador
- MaESP ESP32 OLED de Makerfabs
- Chip: Espressif ESP32 WROOM-32-E
- OLED integrado de 1,3"
- Fuente y más especificaciones: [Makerfabs](https://www.makerfabs.com/makepython-esp32.html?srsltid=AfmBOoo98ESGWyOQi_EoxggwQ4zqeoW0mktzH6rABH1KU28PcvKacGX1)

### 📟 Sensores Compatibles
- **BME280** – temperatura, humedad, presión  
- **BMP280** – temperatura, presión  
- **SHT45** – temperatura, humedad  
- **TMP117** – sensor de temperatura de alta precisión  
- **SSD1306 OLED** – pantalla (I2C, 128x64)  

### ✨ Funciones
- Detección automática de sensores por I2C
- Conexión Wi-Fi (SSID y contraseña en el código)
- Sincronización de hora por NTP
- Registro de datos en CSV (`log.csv`) en memoria interna
- Pantalla alterna entre valores de temperatura y humedad

### 🔌 Conexiones (por defecto en el código)
| Componente  | Pin ESP32 | Nota |
|-------------|-----------|------|
| SDA (I2C)   | GPIO4     | Se puede cambiar en el código |
| SCL (I2C)   | GPIO5     | Se puede cambiar en el código |
| VCC         | 3.3V      | Todos los sensores |
| GND         | GND       | Todos los sensores |

**Direcciones I2C por defecto:**
- BME280 / BMP280 → `0x76` o `0x77`
- SSD1306 OLED → `0x3C`
- SHT45 → `0x44`
- TMP117 → `0x48`

### 🚀 Instalación y uso
1. **Flashear MicroPython en el ESP32**  
   → p. ej., con [Thonny](https://thonny.org) o `esptool.py`
2. **Subir bibliotecas** (`ssd1306.py`, `bmp280.py`, `bme280.py`, `sht4x.py`, `tmp117.py`)
3. Copiar el script principal `main.py` al ESP32
4. Eliminar en `main.py` la siguiente línea:
   ```python
   from config import WIFI_SSID, WIFI_PASSWORD  # Tus credenciales de WiFi
   ```
   Sustituir en main.py `WIFI_SSID` y `WIFI_PASSWORD` por los datos de tu propia red WiFi:
   ```python
   connect_wifi(WIFI_SSID, WIFI_PASSWORD)
   ```
   O bien, ignorar los dos primeros pasos del punto 4 y crear un nuevo archivo config.py con las variables `WIFI_SSID` y `WIFI_PASSWORD` para los datos de tu red WiFi.
5. Iniciar el ESP32 – las lecturas aparecerán en la pantalla OLED y se guardarán en `log.csv`.

---

## English

### 📌 Project Overview
This project demonstrates how an **ESP32** can measure temperature, humidity, and air pressure using various environmental sensors,  
display the data on an **SSD1306 OLED** screen, and store it in a **CSV file** on the ESP32.  

### Microcontroller Board
- MaESP ESP32 OLED by Makerfabs
- Chip: Espressif ESP32 WROOM-32-E
- On-board 1.3" OLED
- Source and more specifications: [Makerfabs](https://www.makerfabs.com/makepython-esp32.html?srsltid=AfmBOoo98ESGWyOQi_EoxggwQ4zqeoW0mktzH6rABH1KU28PcvKacGX1)


### 📟 Supported Sensors
- **BME280** – temperature, humidity, pressure  
- **BMP280** – temperature, pressure  
- **SHT45** – temperature, humidity  
- **TMP117** – high-precision temperature sensor  
- **SSD1306 OLED** – display (I2C, 128x64)  

### ✨ Features
- Automatic I2C sensor detection
- Wi-Fi connection (SSID & password in code)
- Time synchronization via NTP
- CSV data logging (`log.csv`) in internal storage
- Alternating display of temperature and humidity values

### 🔌 Wiring (default in code)
| Component   | ESP32 Pin | Note |
|-------------|-----------|------|
| SDA (I2C)   | GPIO4     | Can be changed in code |
| SCL (I2C)   | GPIO5     | Can be changed in code |
| VCC         | 3.3V      | All sensors |
| GND         | GND       | All sensors |

**Default I2C Addresses:**
- BME280 / BMP280 → `0x76` or `0x77`
- SSD1306 OLED → `0x3C`
- SHT45 → `0x44`
- TMP117 → `0x48`

### 🚀 Installation & Usage
1. **Flash MicroPython onto the ESP32**  
   → e.g., with [Thonny](https://thonny.org) or `esptool.py`
2. **Upload libraries** (`ssd1306.py`, `bmp280.py`, `bme280.py`, `sht4x.py`, `tmp117.py`)
3. Copy the main script `main.py` to the ESP32
4. Delete the following line in `main.py`:
   ```python
   from config import WIFI_SSID, WIFI_PASSWORD  # Your WiFi credentials
   ```
   Replace `WIFI_SSID` and `WIFI_PASSWORD` in `main.py` with your own WiFi network details:
   ```python
   connect_wifi(WIFI_SSID, WIFI_PASSWORD)
   ```
   Or skip the first two steps in 4 and create a new file config.py with the variables `WIFI_SSID` and `WIFI_PASSWORD` containing your WiFi network details.
   5. Start the ESP32 – the measurements will appear on the OLED and be saved in `log.csv`.



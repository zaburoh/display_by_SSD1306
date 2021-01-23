# SSD1306 OLEDモジュール

# I2Cアドレスの確認
コマンド
```bash
$ i2cdetect -y 1
```
出力
```bash
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --    
```

# 必要なライブラリのインストール

## インストール前
```bash
$ pip list
Package       Version
------------- -------
pip           18.1   
pkg-resources 0.0.0  
setuptools    40.8.0 
```

## インストール後
```bash
$ pip install adafruit-circuitpython-ssd1306
```

```bash
$ pip list
Package                          Version
-------------------------------- -------
Adafruit-Blinka                  5.9.2  
adafruit-circuitpython-busdevice 5.0.2  
adafruit-circuitpython-framebuf  1.4.3  
adafruit-circuitpython-ssd1306   2.10.0 
Adafruit-PlatformDetect          2.24.0 
Adafruit-PureIO                  1.1.8  
pyftdi                           0.52.0 
pyserial                         3.5    
pyusb                            1.1.0  
rpi-ws281x                       4.2.5  
RPi.GPIO                         0.7.0  
sysv-ipc                         1.0.1  
```

# PIL for Image, ImageDraw, ImageFont
```bash
$ pip install pillow
```

```bash
$ pip list
Package                          Version
-------------------------------- -------
Pillow                           8.1.0  
```

# smbus2 for BME280
```bash
$ pip install smbus2
```

```bash
$ pip list
Package                          Version
-------------------------------- -------
Adafruit-Blinka                  5.9.2  
smbus2                           0.4.1  
```
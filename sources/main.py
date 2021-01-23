from display import Display
import time
import signal
import sys
from datetime import datetime
from bme280 import BME280

def exit_handler(signal, frame):
  print("\n>> exit handler")
  sys.stdout.write("\n")
  sys.exit(0)

# init
signal.signal(signal.SIGINT, exit_handler)


WIDTH = 128
HEIGHT = 64
BORDER =  5
ADDR = 0x3C

b = BME280()
disp = Display(WIDTH, HEIGHT, BORDER, ADDR)
# disp.draw_border(255, 255)
temp, pres, hum = b.read_data()


while True:
  temp, pres, hum = b.read_data()
  disp.draw_text(
    datetime.now().strftime('%Y/%m/%d (%a)\n%H:%M:%S.%f\n')
    + f'temp :{temp:7.2f}°C\n'
    + f'hum  :{hum:7.2f}%\n'
  )

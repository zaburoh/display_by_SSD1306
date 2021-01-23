from display import Display
import time
import signal
import sys

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

disp = Display(WIDTH, HEIGHT, BORDER, ADDR)
# disp.draw_border(255, 255)

text = "1234567890"

while True: 
  for n in [num for num in range(0, len(text))]:
    disp.draw_text(text[:n])

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class Display():
  def __init__(self, width, height, border, addr):
    self.oled_reset = digitalio.DigitalInOut(board.D4)
    self.WIDTH = width
    self.HEIGHT = height
    self.BORDER = border
    self.i2c = board.I2C()
    
    self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=addr, reset=self.oled_reset)
    self.oled.fill(0)
    self.oled.show()

  def draw_border(self, outline, fill):
    self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=outline, fill=fill)
    self.draw.rectangle(
      (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
      outline = 0,
      fill = 0,
    )
    self.oled.image(self.image)
    self.oled.show()

  def draw_text(self, text):
    image = Image.new("1", (self.oled.width, self.oled.height))
    draw = ImageDraw.Draw(image)

    self.font = ImageFont.load_default()
    (font_width, font_height) = self.font.getsize(text)
    xy = (0, 0)
    draw.multiline_text(
      xy,
      text,
      font = self.font,
      fill = 255,
    )
    self.oled.image(image)
    self.oled.show()



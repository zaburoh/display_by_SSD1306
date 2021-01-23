from smbus2 import SMBus
import time

class BME280():
  def __init__(self):
    self.bus_num = 1
    self.addr = 0x76
    self.bus = SMBus(self.bus_num)

    self.digT = [] # Temp
    self.digP = [] # Pressure
    self.digH = [] # Humidity

    self.t_fine = 0.0

    self.setup()
    self.get_calib_param()

  def setup(self):
    # 0 is measure skip
    osrs_t = 1
    osrs_p = 1
    osrs_h = 1
    # Forced mode 01 | Normal mode 11
    mode = 3
    t_sb = 0
    filter = 0
    spi3w_en = 0

    # [0xF2] 00000001 -> 00000001
    ctrl_hum_reg = osrs_h
    # [0xF4] 00100000 | 00000100 | 00000011 -> 00100111
    ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
    # [0xF5] 00000000 | 00000000 | 00000000 -> 00000000
    config_reg = (t_sb << 5) | (filter << 2) | spi3w_en
    self.write_reg(0xF2, ctrl_hum_reg)
    self.write_reg(0xF4, ctrl_meas_reg)
    self.write_reg(0xF5, config_reg)

  def write_reg(self, addr, data):
    self.bus.write_byte_data(self.addr, addr, data)

  def get_calib_param(self):
    calib = []

    # calib00..calib25 0x88~0xA1
    for i in range(0x88, 0x88 + 24):
      calib.append(self.bus.read_byte_data(self.addr, i))
    calib.append(self.bus.read_byte_data(self.addr, 0xA1))

    # calib26..calib41 0xE1~0xF0
    for i in range(0xE1, 0xE1 + 7 ):
      calib.append(self.bus.read_byte_data(self.addr, i))
    # Temp
    self.digT.append((calib[1] << 8) | calib[0])
    self.digT.append((calib[3] << 8) | calib[2])
    self.digT.append((calib[5] << 8) | calib[4])
    # Pressure
    self.digP.append((calib[7] << 8) | calib[6])
    self.digP.append((calib[9] << 8) | calib[8])
    self.digP.append((calib[11] << 8) | calib[10])
    self.digP.append((calib[13] << 8) | calib[12])
    self.digP.append((calib[15] << 8) | calib[14])
    self.digP.append((calib[17] << 8) | calib[16])
    self.digP.append((calib[19] << 8) | calib[18])
    self.digP.append((calib[21] << 8) | calib[20])
    self.digP.append((calib[23] << 8) | calib[22])
    # Humidity
    self.digH.append(calib[24])
    self.digH.append((calib[26] << 8) | calib[25])
    self.digH.append(calib[27])
    self.digH.append((calib[28] << 4) | (0x0F & calib[29]))
    self.digH.append((calib[30] << 4) | ((calib[29] >> 4) & 0x0F)) 
    self.digH.append(calib[31])

    for i in range(1, 2):
      # 1000 0000 0000 0000
      # ^ ここが1のとき
      if self.digT[i] & 0x8000:
        # 排他的論理和 違うbitの場合に1が立つ
        self.digT[i] = (-self.digT[i] ^ 0xFFFF) + 1

    for i in range(1, 8):
      if self.digP[i] & 0x8000:
        self.digP[i] = (-self.digP[i] ^ 0xFFFF) + 1

    for i in range(0, 6):
      if self.digH[i] & 0x8000:
        self.digH = (-self.digH[i] ^ 0xFFFF) + 1

  def read_data(self):
    data = []
    # data[0] = 0xF7 pres_msb[8bit]
    # data[1] = 0xF8 pres_lsb[8bit]
    # data[2] = 0xF9 pres_xlsb[8bit]
    # data[3] = 0xFA temp_msb[8bit]
    # data[4] = 0xFB temp_lsb[8bit]
    # data[5] = 0xFC temp_xlsb[8bit]
    # data[6] = 0xFD hum_msb[8bit]
    # data[7] = 0xFE hum_lsb[8bit]
    for i in range(0xF7, 0xF7+8):
      data.append(self.bus.read_byte_data(self.addr, i))

    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw = (data[6] << 8) | data[7]

    return (self.compensate_T(temp_raw), self.compensate_P(pres_raw), self.compensate_H(hum_raw))

  def compensate_T(self, adc_T):
    v1 = (adc_T / 16384.0 - self.digT[0] / 1024.0) * self.digT[1]
    v2 = (adc_T / 131072.0 - self.digT[0] / 8192.0) * (adc_T / 131072.0)
    self.t_fine = v1 + v2
    temperature = self.t_fine / 5120.0
    # print(f'temp: {temperature:7.2f} C')
    return temperature

  def compensate_P(self, adc_P):
    pressure = 0.0

    v1 = (self.t_fine / 2.0) - 64000.0
    v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * self.digP[5]
    v2 = v2 + ((v1 * self.digP[4]) * 2.0)
    v2 = (v2 / 4.0) + (self.digP[3] * 65536.0)
    v1 = (((self.digP[2] * (((v1 / 4.0) * (v1 /4.0)) / 8192)) / 8) + ((self.digP[1] * v1) / 2.0)) / 262144
    v1 = ((32768 + v1) * self.digP[0]) / 32768

    if v1 == 0:
      return 0

    pressure = ((1048576 - adc_P) - (v2 / 4096)) * 3125
    if pressure < 0x800000000:
      pressure = (pressure * 2.0) / v1
    else:
      pressure - (pressure / v1) * 2

    v1 = (self.digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
    v2 = ((pressure / 4.0) * self.digP[7]) / 8192.0
    pressure = pressure + ((v1 + v2 + self.digP[6]) / 16.0)

    # print(f'pressure : {pressure / 100:-6.2f} hPa')

    return pressure/100

  def compensate_H(self, adc_H):
    var_h = self.t_fine - 76800.0
    if var_h != 0:
      var_h = (adc_H - (self.digH[3] * 64.0 + self.digH[4] / 16384.0 * var_h)) * (self.digH[1] / 65536.0 * (1.0 + self.digH[5] / 67108864.0 * var_h * (1.0 + self.digH[2] / 67108864.0 * var_h)))
    else:
      return 0

    var_h = var_h * (1.0 - self.digH[0] * var_h / 524288.0)

    if var_h > 100.0:
      var_h = 100.0
    elif var_h < 0.0:
      var_h = 0.0
    # print(f'hum : {var_h:6.2f} %')

    return var_h


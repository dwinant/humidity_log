import pigpio
import smbus
import time

BAUD = 1000
I2C_ADDR = 0x40
I2C_BUS = 1

pi = pigpio.pi()

def swap16 (data):
    return ((data & 0xFF) << 8) | ((data >> 8) & 0xFF)

class si7021:
    def humidity (self):
        self.hdata = self.read_command (0xE5)
        return self.hdata * 125 / 65536.0 - 6

    def temperature (self):
        self.tdata = self.read_command (0xE0)
        return self.tdata * 175.72 / 65536.0 - 46.85

    def show_values (self):
        h = self.humidity()
        print ("Humidity    %7.2f %%    [%04x]" % (h, self.hdata))
        t = self.temperature()
        print ("Temperature %7.2f C    [%04x]" % (t, self.tdata))

class si_7021_soft (si7021):
    def __init__ (self, id, SDA, SCL):
        self.id = id
        self.SDA = SDA
        self.pi = pigpio.pi()
        try:
            self.pi.bb_i2c_close (SDA)
        except:
            pass
        self.pi.bb_i2c_open (SDA, SCL, BAUD)

    def close (self):
        self.pi.bb_i2c_close (self.SDA)
        
    def read_command (self, command):
        data = self.pi.bb_i2c_zip (self.SDA, [ 4,I2C_ADDR, 2,7,1,command, 2,6,2, 3,0])
        if len(data) < 2: raise "Bad format returned"
        if data[0] < 0: raise "I2C failed with error %d" % data[0]
        if data[0] < 2: raise "First data is %d which is less than 2" % data[0]
        if len(data[1]) < 2: raise "not enough data in bytearray"
        data = data[1]
        return data[0] * 256 + data[1]

class si_7021_hard (si7021):
    def __init__ (self, id):
        self.id = id
        self.bus = smbus.SMBus(I2C_BUS)

    def close (self):
        self.bus.close()

    def read_command (self, command):
        data = self.bus.read_word_data (I2C_ADDR, command)
        return swap16(data)

        
def test():
    si1 = si_7021_soft (22, 23)
    si2 = si_7021_hard()

    try:
        print ("soft on 22/23")
        si1.show_values()
        print ("hard on I2C")
        si2.show_values()
    finally:
        si1.close()
        si2.close()


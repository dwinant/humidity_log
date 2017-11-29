
# This logger uses code from ControlEverything.com, which was provided with the following note:
  # Distributed with a free-will license.
  # Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
  # SI7021
  # This code is designed to work with the SI7021_I2CS I2C Mini Module available from ControlEverything.com.
  # https://www.controleverything.com/content/Humidity?sku=SI7021_I2CS#tabs-0-product_tabset-2
#

import smbus
import socket
import time

LOG_INTERVAL_MINUTES = 5
I2C_BUS = 1
LOG_FILE = '/home/pi/humidity/humidity.log'

# Derived Values
_LOG_INTERVAL_SECONDS = LOG_INTERVAL_MINUTES * 60

# Get I2C bus
bus = smbus.SMBus(I2C_BUS)
host = socket.gethostname()

def read_humidity_and_temperature():
    # SI7021 address, 0x40(64)
    #		0xF5(245)	Select Relative Humidity NO HOLD master mode
    bus.write_byte(0x40, 0xF5)

    time.sleep(0.1)

    # SI7021 address, 0x40(64)
    # Read data back, 2 bytes, Humidity MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

    # Convert the data
    humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

    time.sleep(0.1)

    # SI7021 address, 0x40(64)
    #		0xE0(224)	Select temperature (read after humidity)
    bus.write_byte(0x40, 0xE0)

    time.sleep(0.1)

    # SI7021 address, 0x40(64)
    # Read data back, 2 bytes, Temperature MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

    # Convert the data
    cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    fTemp = cTemp * 1.8 + 32

    return humidity, cTemp


def log (msg):
    with open(LOG_FILE, 'a') as logf:
        logf.write (msg + "\n")
    print (msg)
    
log ("Host,Time,Humidity (%),Temperature (C)")
while True:
    # Output data to screen
    h,t = read_humidity_and_temperature()
    log ("%s, %s,%7.2f,%7.2f" % (host,time.strftime("%Y-%m-%d %H:%M:%S"), h, t))

    time.sleep (_LOG_INTERVAL_SECONDS)

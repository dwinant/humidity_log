
# This logger uses code from ControlEverything.com, which was provided with the following note:
  # Distributed with a free-will license.
  # Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
  # SI7021
  # This code is designed to work with the SI7021_I2CS I2C Mini Module available from ControlEverything.com.
  # https://www.controleverything.com/content/Humidity?sku=SI7021_I2CS#tabs-0-product_tabset-2
#

import smbus
import socket
import sys
import time
from si_7021 import si_7021_soft, si_7021_hard

LOG_INTERVAL_MINUTES = 5
LOG_FILE = '/home/pi/humidity_log/humidity.log'
CFG_FILE = '/home/pi/humidity.cfg'

# Derived Values
_LOG_INTERVAL_SECONDS = LOG_INTERVAL_MINUTES * 60
host = socket.gethostname()
sensors = []

def log (msg):
    with open(LOG_FILE, 'a') as logf:
        logf.write (msg + "\n")
    print (msg)

def soft_reset ():
    bus.write_byte (I2C_ADDR, 0xFE)
    print "sent a soft reset"

def hold_master_read ():
    data0 = bus.read_word_data (I2C_ADDR, 0xE5)
    data1 = swap16 (data0)
    humidity = data1 * 125 / 65536.0 - 6
    print "read humidity %04X %04X = %7.2f %%" % (data0, data1,  humidity)

    data0 = bus.read_word_data (I2C_ADDR, 0xE3)
    data1 = swap16 (data0)
    cTemp = (data1 * 175.72 / 65536.0) - 46.85
    print "read temperature %04x %04x = %7.2f C" % (data0, data1, cTemp)
    

def get_info ():
    for s in sensors:
        print ("Info for sensor %s on host %s" % (s.id, host))
        try:
            print ("  user control byte   %02X" % s.read_control())
            print ("  heater control byte %02X" % s.read_heater())
            print ("  firmware rev        %02X" % s.read_firmware_rev())
        except:
            print ("   I2C failed")

def check_loop ():
    try:
        while True:
            for s in sensors:
                print ("Checking sensor %s on host %s" % (s.id, host))
                try:
                    # Output data only to screen
                    h = s.humidity()
                    t = s.temperature()
                    print ("%s  HUM = %7.2f %%  TMP = %7.2f C" % (time.strftime("%Y-%m-%d %H:%M:%S"), h, t))
                    time.sleep(2)
                except SystemError:
                    print ("  I2C error")
    except KeyboardInterrupt:
        print "\ndone"

def log_main ():    
    try:
        log ("Host,Time,Humidity (%),Temperature (C)")
        while True:
            for s in sensors:
                try:
                    # Output data to screen and log
                    h = s.humidity()
                    t = s.temperature()
                    log ("%s, %s,%7.2f,%7.2f" % (s.id,time.strftime("%Y-%m-%d %H:%M:%S"), h, t))
                except SystemError:
                    log ("%s, %s  I2C error" % (s.id, time.strftime("%Y-%m-%d %H:%M:%S")))

            time.sleep (_LOG_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print "\ndone"

def read_config_line (line):
    flds = line.rstrip().split(',')
    if len(flds) == 3:
        sensors.append (si_7021_soft (flds[0], int(flds[1]), int(flds[2])))
    elif len(flds) == 1:
        sensors.append (si_7021_hard (flds[0]))
    else:
        raise ValueError ("invalid configuration in file %s" % CFG_FILE)
    
def read_config():
    #try:
        with open(CFG_FILE, 'r') as f:
            for line in f:
                if not line.startswith('#'):
                    read_config_line (line)
    #except:
    #    print ("Could not read config file %s, assuming single sensor named %s" % (CFG_FILE, host))
    #    sensors.append (si_7021_hard(host))

read_config()
print ("found %d sensors" % len(sensors))
for s in sensors:
    print ("  %s" % (s.id))
    
if len(sys.argv) > 1:
    if sys.argv[1] == 'info':
        get_info()
    elif sys.argv[1] == 'reset':
        soft_reset()
    elif sys.argv[1] == 'check':
        check_loop()
    elif sys.argv[1] == 'read':
        hold_master_read()
    else:
        print "unknown argument, try info, read, reset or check"
else:
    log_main()


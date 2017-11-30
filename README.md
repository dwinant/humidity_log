# humidity_log

## Introduction

This project logs humidity & temperature readings on a Raspberry Pi with 
an Si7021 humidity sensor connected via I2C.

The log data can optionally be uploaded to DropBox on a regular basis
using the DropBox_Uploader project from andreafabrizi, https://github.com/andreafabrizi/Dropbox-Uploader

The idea is to use the Raspberry Pi headless, but connected to the Internet via cabled Ethernet or WiFi. Then it is able to upload reports which you can access via DropBox from anywhere. Or you could skip the upload and just connect to the device to read the logfile.

## Usage
The package consists of two pieces, the logger and the uploader.


### Logger
The logger is a Python script which reads the humidity and temperature from the Si7021 sensor at regular intervals and logs the data to stdout and to a specific file.

You can change the interval and the filename by editing the Python. Even if you aren't a Python programmer it should be straightforward.

### Uploader
The uploader is a shell script, meant to be run by cron, which logs for the log file produced by the logger. If it finds the file, it uploads the contents to Dropbox and removes it. There's also a local archive of the data saved.  As it uploads to Dropbox, it creates a new filename which include the hostname and a timestamp, so old files won't be overwritten by new files.

## Example

When you startup the logger, it will show a header line and the first temperature and humidity reading, like so:
> Host,Time,Humidity (%),Temperature (C)
> node1, 2017-11-28 23:01:20,  36.16,  20.68

## Setup

### Setup Raspberry Pi

Set the hostname as you wish, and make sure the I2C interface is enabled in 
Preference / Raspberry Pi Configuration / Interfaces.

### Download Dropbox-Uploader

See: https://github.com/andreafabrizi/Dropbox-Uploader

> git clone https://github.com/andreafabrizi/Dropbox-Uploader.git
> chmod +x Dropbox-Uploader/dropbox_uploader.sh

### Setup Dropbox-Uploader

Run the uploader once using the account which will be 
doing the regular uploads so that you can configure
the DropBox App token.

### Download the Humidity Logger

> git clone https://github.com/dwinant/humidity_log.git

### Test the logger, I2C and your sensor device

> python humidity_log.py check

You should see output every couple seconds as it reads the sensor.

### Set the logger to automatically start

To auto-start the logger, add a command similar to this
to your /etc/rc.local file

> sudo -u pi python /home/pi/humidity/humidity_log.py &

### Schdule the Uploader regularly

To run the uploader every hour, add this line to /etc/crontab:
> 0  *    * * *   pi      /home/pi/humidity/upload_log.sh

or for uploads every 6 hours use:
> 0  1,7,13,19    * * *   pi      /home/pi/humidity/upload_log.sh

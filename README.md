# humidity_log

Introduction

This project logs humidity & temperature readings on a Raspberry Pi with 
an Si7021 humidity sensor connected via I2C.

The log data can optionally be uploaded to DropBox on a regular basis
using the DropBox_Uploader project from andreafabrizi, https://github.com/andreafabrizi/Dropbox-Uploader


Setup

Setup Raspberry Pi

Set the hostname as you wish, and make sure the I2C interface is enabled in 
Preference / Raspberry Pi Configuration / Interfaces.

Download Dropbox-Uploader

See: https://github.com/andreafabrizi/Dropbox-Uploader

git clone https://github.com/andreafabrizi/Dropbox-Uploader.git
chmod +x Dropbox-Uploader/dropbox_uploader.sh

Setup Dropbox-Uploader

Run the uploader once using the account which will be 
doing the regular uploads so that you can configure
the DropBox App token.

Download the Humidity Logger

git clone https://github.com/dwinant/humidity_log.git

Set the logger to automatically start

To auto-start the logger, add a command similar to this
to your /etc/rc.local file

sudo -u pi python /home/pi/humidity/humidity_log.py &

Run the Uploader regularly

To run the uploader every hour, add this line to /etc/crontab:
0  *    * * *   pi      /home/pi/humidity/upload_log.sh






# set hostname
# get dropbox_uploader
# get humidity_logger

git clone https://github.com/andreafabrizi/Dropbox-Uploader.git
chmod +x Dropbox-Uploader/dropbox_uploader.sh

# run the uploader once using the account which will be 
# doing the regular uploads so that you can configure
# the DropBox App key


# to auto-start the logger, add a command similar to this
# to your /etc/rc.local file
sudo -u pi python /home/pi/humidity/humidity_log.py &

# to run the uploader every hour, add this line to 
# /etc/crontab
0  *    * * *   pi      /home/pi/humidity/upload_log.sh






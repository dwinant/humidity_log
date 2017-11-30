#/bin/sh

DIR=/home/pi/humidity
LOG=$DIR/humidity.log
TMP=$DIR/humidity.tmp
SAV=$DIR/humidity.logged
RDY=$DIR/humidity.ready
UPL=data/humidity_`uname -n`_`date +%Y%m%d_%H%M%S`.log

UPLOAD="/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload "

if [ -f $TMP ]; then rm -f $TMP; fi

if [ -f $LOG ]; then
  # immediately rename in case logger runs while we are uploading
  mv $LOG $TMP
  cat $TMP >> $RDY
  cat $TMP >> $SAV
  rm $TMP
fi

if [ -f $RDY ]; then
  # upload the ready file as a new DropBox file
  $UPLOAD $RDY $UPL
  if [ "$?" = "0" ]; then
    rm $RDY
  fi
  echo Done
fi


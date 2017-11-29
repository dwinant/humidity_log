#/bin/sh

DIR=/home/pi/humidity
LOG=$DIR/humidity.log
TMP=$DIR/humidity.tmp
SAV=$DIR/humidity.logged
RDY=$DIR/humidity.ready
UPL=$DIR/humidity_`uname -n`_`date +%Y%m%d_%H%M%S`.log

if [ -f $TMP ]; then rm -f $TMP; fi

echo UPL is $UPL
exit 0

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
  rm $RDY
fi


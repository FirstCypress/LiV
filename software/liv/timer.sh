#!/bin/bash

sleep 10

pid=`ps aux |grep Adafruit | grep -v grep | awk '{print $2}'`

if [ -z "$pid" ]
 then
  echo "NO SUCH PROCESS"
 else
  sudo kill -9 $pid
  echo "KILLED ADAFRUIT PROCESS"
fi


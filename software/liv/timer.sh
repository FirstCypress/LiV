#!/bin/bash

sleep 10

pid=`ps aux |grep Adafruit | grep -v grep | awk '{print $2}'`

if [ -z "$pid" ]
 then
  echo "NO HANGED ADAFRUIT PROCESS"
 else
  sudo kill -9 $pid
  echo "KILLED HANGED ADAFRUIT PROCESS"
fi


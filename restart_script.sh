#!/bin/bash  
# Restart script if not running (error caused failure)
if pgrep -lf python | grep mojo.py ; then
 :
else 
  sudo python /home/pi/mojo_home_bot/mojo.py &
fi

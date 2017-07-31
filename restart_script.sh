#!/bin/bash  
# Restart script if not running (error caused failure)
if pgrep -f main.py ; then
   :
else 
   sudo python /home/pi/virtual_assistant/main.py startx &
fi

#!/bin/bash  
# Restart script if not running (error caused failure)
if pgrep -f main.py ; then
   :
else
   sudo python3 /home/mojo/virtual_assistant/main.py startx >> /home/mojo/virtual_assistant/files/assistant_debug.log 2>&1 &
fi

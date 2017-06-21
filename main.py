#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
from assistant import Assistant

# If method call defined on launch, call. 'startx' = listen for commands from telegram
# @todo allow for all responders to execute concurrently depending on settings.
# Start assistant with telegram
if len(sys.argv) == 2 and sys.argv[1] == 'startx':  # pragma: no cover
    bot = Assistant(mode='telegram')
    bot.listen()
# Start with audio responder
elif len(sys.argv) == 2 and sys.argv[1] == 'audio':
    bot = Assistant(mode='audio')
    bot.listen()
# Start with console responder
elif (len(sys.argv) == 1 and 'unittest' not in sys.argv[0]) or (len(sys.argv) == 2 and sys.argv[1] != 'discover'):  # pragma: no cover
    bot = Assistant(mode='console')
    bot.listen()


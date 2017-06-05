#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
import schedule
import datetime
from mojo import Mojo


def execute_bot_command(bot, command):
    msg = {"chat": {"id": bot.admin}, "text": command}
    bot.handle(msg)


def execute_bot_command_monthly(bot, command):
    now = datetime.datetime.now()
    if now.day == 1:
        execute_bot_command(bot, command)


# If method call defined on launch, call. 'startx' = listen for commands from telegram
# Start mojo
if len(sys.argv) == 2 and sys.argv[1] == 'startx':  # pragma: no cover
    bot = Mojo()
    # Load scheduled tasks
    schedule.clear()
    # schedule.every().minute.do(execute_bot_command, 'is house empty')
    schedule.every(10).minutes.do(execute_bot_command, bot, 'get recent transactions')
    schedule.every().day.at("00:00").do(execute_bot_command, bot, 'rotate log')
    schedule.every().day.at("6:30").do(execute_bot_command, bot, 'morning')
    schedule.every().day.at("8:30").do(execute_bot_command, bot, 'morning others')
    schedule.every().day.at("13:00").do(execute_bot_command, bot, 'new properties')
    schedule.every().day.at("7:00").do(
        execute_bot_command_monthly,
        bot,
        '-700 budget')  # reset budget at beginning of month
    bot.listen()
# Execute command without listening (ignore discover unittest)

elif (len(sys.argv) == 1 and 'unittest' not in sys.argv[0]) or (len(sys.argv) == 2 and sys.argv[1] != 'discover'):  # pragma: no cover
    bot = Mojo()
    bot.listen(mode='console')


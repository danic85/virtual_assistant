#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
import schedule
import datetime
from assistant import Assistant


def execute_bot_command(bot, command):
    msg = {"chat": {"id": bot.admin}, "text": command}
    bot.handle(msg)


def idle_behaviours(bot):
    bot.idle_behaviours()


def execute_bot_command_monthly(bot, command):
    now = datetime.datetime.now()
    if now.day == 1:
        execute_bot_command(bot, command)


# If method call defined on launch, call. 'startx' = listen for commands from telegram
# Start assistant with telegram
if len(sys.argv) == 2 and sys.argv[1] == 'startx':  # pragma: no cover
    bot = Assistant(mode='telegram')
    # Load scheduled tasks
    schedule.clear()
    # schedule.every().minute.do(execute_bot_command, 'is house empty')
    # schedule.every(10).minutes.do(execute_bot_command, bot, 'get recent transactions')
    schedule.every(5).minutes.do(idle_behaviours, bot)
    #schedule.every().day.at("00:00").do(execute_bot_command, bot, 'rotate log')
    #schedule.every().day.at("6:30").do(execute_bot_command, bot, 'morning')
    #schedule.every().day.at("8:30").do(execute_bot_command, bot, 'morning others')
    schedule.every().day.at("13:00").do(execute_bot_command, bot, 'new properties')
    schedule.every().day.at("7:00").do(
        execute_bot_command_monthly,
        bot,
        '-700 budget')  # reset budget at beginning of month
    bot.listen()
# Start with audio responder
elif len(sys.argv) == 2 and sys.argv[1] == 'audio':
    bot = Assistant(mode='audio')
    bot.listen()
# Start with console responder
elif (len(sys.argv) == 1 and 'unittest' not in sys.argv[0]) or (len(sys.argv) == 2 and sys.argv[1] != 'discover'):  # pragma: no cover
    bot = Assistant(mode='console')
    bot.listen()


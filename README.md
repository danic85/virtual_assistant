# Mojo Home Assistant
[ ![Codeship Status for danic85/mojo_home_bot](https://app.codeship.com/projects/b6100e40-bf03-0134-1010-1ebff7fcacc1/status?branch=master)](https://app.codeship.com/projects/196463)

A home automation bot via telegram

## Features
- Natural language commands
- Telegram integration
- Feed parsing
- Raspberry Pi compatibile
- Camera and PIR sensor integration
- Chat bot

## Commands
- "What time is it / what is the time / time": Current time 
- "Help / List commands / command list": Show all commands with regex
- "Weather": Get current weather for preconfigured location
- "Word of the day": Return a word of the day with definition
- "Check fibre": Parse html site and notify if fibre broadband availabilty changes
- "Update": Automatic self-update from git
- "News": Top 5 BBC News stories
- "Morning / Morning Others": Configurable wake-up message at predefined time, daily.
- "Camera": Take photo from Raspberry Pi camera and send to user via telegram.
- "Video": Record short video from Raspberry Pi camera and send to user via telegram.
- "Get Log": Retrieve log file for inspection via telegram
- "[amount] [expense type]": Log expense of x amount of y type, convert to GBP from USD if $ included in price (e.g. '$100 tickets').
- "Budget": Show remaining monthly budget
- "Get Expenses": Download current and previous month's expenses in CSV format via telegram.
- "Broadcast [message]": Send message to all users
- "Riddle / Riddle Answer": Return a random riddle. Return answer to riddle
- "Goodbye / We're going out / Bye / Security On": Enable home security (authorised users only)
- "Hello / We're back/home/here /Security Off": Disable home security (authorised users only)
- "Is house empty": Check wifi network for connected devices to determine occupancy.
- "Sweep": Check PIR sensor for movement.
- "Override Security": Disable automatic security
- "Shower thought": Return random thought of the day from Reddit

## Unit testing
Execute `python -m unittest discover` in the project directory to run all unit tests

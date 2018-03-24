# Python Virtual Assistant
[ ![Codeship Status for danic85/virtual_assistant](https://app.codeship.com/projects/b6100e40-bf03-0134-1010-1ebff7fcacc1/status?branch=master)](https://app.codeship.com/projects/196463)

A home automation bot via telegram

## Features
- Natural language commands
- Telegram integration including optional voice recognition and text-to-speech response
- Feed parsing
- Raspberry Pi compatible
- Camera and PIR sensor integration
- Chat bot
- Compatible with Python 2 and Python 3

## Commands
### Countdown
- `Countdown dd-mm-yyyy <event name>`: Start counting down to an event.
- `Get countdowns`: List all active countdowns
- `Get closest countdowns`: List the two closest active countdowns
### Dictionary
- `Word of the day`: Return a word of the day with definition
### Echochat
The Echochat behaviour is a simple machine learning algorithm that allows users to build a database of possible responses to phrases.
This behaviour is the last to be executed meaning that an un-matched command will be handled by Echochat.
- `Train echochat`: Chatbot will send a message to the user and wait for a response for the purposes of traing
### Expenses
- `<amount> <expense type>`: Log expense of x amount of y type, convert to GBP from USD if $ included in price (e.g. '$100 tickets').
- `Budget`: Show remaining monthly budget
- `Get Expenses`: Download current and previous month's expenses in CSV format via telegram
### General
- `What time is it / what is the time / time`: Current time
- `Set config <key>=<value>` Set a key value config pair
- `Help / List commands / command list`: Show all commands
- `Update`: Automatic self-update from git
- `Emergency shutdown`: Exit the program and shutdown the OS
- `Emergency reboot`: Exit the program and reboot the OS
- `Good Morning / Morning`: Configurable wake-up message at predefined time, daily.
- `Get Log`: Retrieve log file for inspection via telegram
- `Rotate Log`: Backup log nightly. Logs are stored for 1 week
- `Broadcast <message>`: Send message to all users
- `Exit / Quit`: Safely exit program
### Monzo Integration
- `add monzo token <auth_code> <client_id> <client_secret>`: Add a Monzo authentication for 'Get Transactions' command.
- `Get Transactions`: Downloads all transactions from authenticated monzo accounts, remove expired access tokens and notify of any new transactions.
- `Get Recent Transactions`: As above, but limited to the last day
### News
- `News`: Top news stories from selected sources (defined in config)
- `News sources`: Get list of news sources for configuration
### Camera
Required: RPI Camera
- `Camera / Big Photo / What's going on / Night vision`: Take photo from Raspberry Pi camera and send to user via telegram.
- `Video`: Record short video from Raspberry Pi camera and send to user via telegram.
- `Timelapse`: Take a photo every 5 minutes. Stop with `Stop Timelapse`
### Security
Required: RPI Camera, HC-SR501 PIR Motion Sensor
Connect `Pin 4` to HC-SR501 PIR Motion Sensor (see http://www.rototron.info/using-a-motion-detector-on-raspberry-pi/ for guide).
Connect `Pin 17`  to LED to indicate motion (when security on).
- `Security On`: Enable security system. When motion is detected send picture to admin.
- `Security Off`: Disable security system
- `test security`: Light up LED when motion detected, but do not take picture
### Reddit
- `Thought of the day`: Return random thought of the day from Reddit r/showerthoughts
- `Did you know / Teach me something`: Return a random did you know from Reddit r/didyouknow
- `Funny Image`: Return a funny image and caption from Reddit r/funny
### Reminder
- `Remind me/us <when> to <task>`: Set a reminder
- `Check reminders`: notify user of any due reminders
- `Output reminders`: JSON output of all reminders currently in system (for debug)
### Take Turns
- `Who's turn is it?`: Is it my turn tonight (this is an example class that can be updated to meet requirements)
### Universal Translator
- `Translate <something> to <language>` - Translate a phrase to a specified language
- `Translate <something> from <language>` - Translate a phrase from a specified language to English
### Weather
- `Weather`: Get current weather for preconfigured location
- `Weather Forecast`: Get a 5 day forecast for rain or ice
- `Detailed Forecast / Detailed forecast for the next <days> days`: Get a detailed forecast over a defined period (defaulted to 2 days)
### Zoopla Property Search
- `Properties`: Specific property search via Zoopla. This is an example class that can be modified
- `New Properties`: Only notify the user of new properties that match the search

## Idle Behaviour
The virtual assistant is able to run tasks in the background at pre-defined times. Currently the following tasks will be executed:
- Export database every night at midnight
- Train Echochat every 2 - 36 hours
- Rotate log every night at midnight
- Send Morning message every morning at 8am
- Check for recent monzo transactions every 5 minutes (every time `idle` is called)
- Send a 'did you know' message to users every 100 - 200 hours
- Send a 'thought of the day' message to users every 50 - 120 hours
- Send a funny image to users every 24 - 72 hours
- Check reminders and notify users of due reminders every 5 minutes (every time `idle` is called)
- Check for new Zoopla properties every day at 1pm

## Getting Started
1. `git clone https://github.com/danic85/virtual_assistant.git`
2. Navigate to directory `virtual_assistant`
3. `pip3 install -r requirements.txt`
4. `apt-get install mongodb` to install the database
5. `sudo apt-get install -y gpac` to install mp4box for video capture

## Install PocketSphinx (only needed for voice recognition)
1. wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download -O sphinxbase.tar.gz
2. wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download -O pocketsphinx.tar.gz
3. tar -xzvf sphinxbase.tar.gz
4. tar -xzvf pocketsphinx.tar.gz
5. sudo apt-get install bison libasound2-dev swig
6. cd sphinxbase-5prealpha
7. ./configure --enable-fixed
8. make
9. sudo make install
10. cd ../pocketsphinx-5prealpha
11. ./configure
12. make
13. sudo make install
14. sudo apt-get install -qq python python-dev python-pip build-essential swig libpulse-dev
15. sudo pip install pocketsphinx

## Add Configuration Keys
Enter the command `set config <key>=<value>` for the following keys:
- Users=<user_id1>,<user_id2>: List of Telegram user IDs to grant access to
- Admin=<user_id>: Telegram User ID (REQUIRED for telegram integration)
- Telbot=<telegram_bot_key>: Telegram Bot Key https://core.telegram.org/bots (REQUIRED for telegram integration)
- OpenWeatherMapKey=<owm_key>: Location key from Open Weather Map
- OpenExchangeRatesKey=<open_exchange_rates_key>: Key for Open Exchange Rates
- News=<source_one>,<source_two>: Comma separated list of news sources from newsapi.org
- NewsAPIKey=<newsapi_key>: newsapi.org key
- ZooplaAPI=<zoopla_api_key>: API key for zoopla

### Execute command from the terminal
To execute a command, run `python3 main.py` and then enter the command at the prompt

### Initialize with Telegram
1. Execute `python3 main.py startx`

### Start on Boot
1. Add `(sleep 10; python3 /home/pi/virtual_assistant/main.py startx) &` to `/etc/rc.local` replacing path if appropriate.

## Unit testing
Execute `python3 -m unittest discover` in the project directory to run all unit tests

### Code Coverage
* Execute `coverage run -m unittest discover` to run all tests with coverage
* To display coverage report execute `coverage report`. A list of omitted directories and lines are included in .coveragerc

### Monzo
* Sign in to developers.monzo.com
* Authorise access via email
* Create new OAuth client with a redirect url of http://localhost
* Get your access token by navigating to https://auth.getmondo.co.uk/?client_id=<client_id>&redirect_uri=http://localhost&response_type=code&state=<unique_string>
* Authorise access via email
* Extract code from return URL
* Send message to Assistant "add monzo token <auth_code> <client_id> <client_secret>" (case is important here!)
* Wait for transactions or Send 'Get Transactions'

### Restart Script
There are some issues currently that cause unhandled exceptions which trigger an exit. the `restart_script.sh` bash script will watch for the main.py file running as a process, and restart it if it fails. 
* Edit `restart_script.sh` to use the correct path
* `crontab -e`
* Add `0 * * * * <path_to_restart_script.sh>` to the crontab file. This will execute the script every hour.

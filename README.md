# Mojo Home Assistant
[ ![Codeship Status for danic85/mojo_home_bot](https://app.codeship.com/projects/b6100e40-bf03-0134-1010-1ebff7fcacc1/status?branch=master)](https://app.codeship.com/projects/196463)

A home automation bot via telegram

## Features
- Natural language commands
- Telegram integration including optional voice recognition and text-to-speech response
- Feed parsing
- Raspberry Pi compatible
- Camera and PIR sensor integration
- Chat bot
- Integrated [Braillespeak](https://github.com/danic85/braillespeak) on responses 

## Commands
### General
- "What time is it / what is the time / time": Current time 
- "Help / List commands / command list": Show all commands with regex
- "Update": Automatic self-update from git
- "Morning / Morning Others": Configurable wake-up message at predefined time, daily.
- "Get Log": Retrieve log file for inspection via telegram
- "Broadcast [message]": Send message to all users
### Feeds
- "Weather": Get current weather for preconfigured location
- "Word of the day": Return a word of the day with definition
- "Check fibre": Parse html site and notify if fibre broadband availability changes
- "News": Top 5 BBC News stories
- "Riddle / Riddle Answer": Return a random riddle. Return answer to riddle
- "Thought of the day": Return random thought of the day from Reddit r/showerthoughts
- "Did you know / Teach me something": Return a random did you know from Reddit r/didyouknow
### Camera
Required: RPI Camera
- "Camera": Take photo from Raspberry Pi camera and send to user via telegram.
- "Video": Record short video from Raspberry Pi camera and send to user via telegram.
### Budgetting
- "[amount] [expense type]": Log expense of x amount of y type, convert to GBP from USD if $ included in price (e.g. '$100 tickets').
- "Budget": Show remaining monthly budget
- "Get Expenses": Download current and previous month's expenses in CSV format via telegram
#### Monzo Integration
- "Add Monzo Token <access token>": Add a Monzo access token for 'Get Transactions' command (these are just stored in memory). Get token from https://developers.monzo.com/api/playground
- "Get Transactions": Downloads new transactions from authenticated monzo accounts, remove expired access tokens and notify of any new transactions.
### Countdown
- "Countdown dd-mm-yyyy [event name]": Start counting down to an event.
- "Get countdowns": List all active countdowns
### Security
Required: RPI Camera, HC-SR501 PIR Motion Sensor
Connect `Pin 4` to HC-SR501 PIR Motion Sensor (see http://www.rototron.info/using-a-motion-detector-on-raspberry-pi/ for guide).
Connect `Pin 17`  to LED to indicate motion (when security on).
- "Goodbye / We're going out / Bye / Security On": Enable security system. When motion is detected send picture to admin.
- "Hello / We're back/home/here /Security Off": Disable security system
- "test security": Light up LED when motion detected, but do not take picture

## Getting Started
1. `git clone https://github.com/danic85/mojo_home_bot.git`
2. Navigate to directory `mojo_home_bot`
3. `pip install -r requirements.txt`
4. `sudo apt-get install libav-tools` and `sudo apt-get install flac` (Required for pydub as part of speech recognition)

### Execute command from the terminal
To execute a command, run `python mojo.py 'the command'` (e.g. `python mojo.py 'time'`)

### Initialize with Telegram
1. Rename the config file: `mv config.ini.example config.ini`
2. Complete the config.ini file: 
  * Name: The Bot's Name
  * Telbot: Telegram Bot Key https://core.telegram.org/bots (REQUIRED for telegram integration)
  * Admin: Telegram User ID (REQUIRED for telegram integration)
  * AdminName: Your name
  * FibreTel: Telephone number for fibre broadband availability checker
  * OpenWeatherMapKey: Location key from Open Weather Map
  * Users: Telegram User IDs, comma separated
  * OpenExchangeRatesKey: Key for Open Exchange Rates
  * RouterIP: Your router's IP (for automatic security check)
  * MacAddresses: List of MAC addresses to detect on network (for automatic security check)
  * BraillespeakPort: The serial port to connect to braillespeak arduino (e.g. `/dev/ttyUSB0`)
3. `python mojo.py startx`

### Start on Boot
1. Add execute permission to mojo.py `chmod +x mojo.py`
2. Add `(sleep 10; python /home/pi/mojo_home_bot/mojo.py startx) &` to `/etc/rc.local` replacing path if appropriate.

### Restart script
This project is a WIP. Occasionally the script may exit due to an unhandled exception. Enable `restart_script.sh` to check for the process and restart if necessary: (Optional)
1. `chmod +x restart_script.sh`
2. `sudo crontab -e` 
3. Add `30 * * * * sudo python /home/pi/mojo_home_bot/restart_script.sh` 

## Unit testing
Execute `python -m unittest discover` in the project directory to run all unit tests

### Code Coverage
* Execute `coverage run -m unittest discover` to run all tests with coverage
* To display coverage report execute `coverage report`
* Omit directories from the report with the `--omit` flag. E.g. `coverage report  --omit=/home/rof/.virtualenv/lib/python2.7/site-packages/*`


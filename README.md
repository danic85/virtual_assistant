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
- Compatible with Python 2 and Python 3

## Commands
### General
- "What time is it / what is the time / time": Current time 
- "Help / List commands / command list": Show all commands
- "Update": Automatic self-update from git
- "Morning / Morning Others": Configurable wake-up message at predefined time, daily.
- "Get Log": Retrieve log file for inspection via telegram
- "Broadcast [message]": Send message to all users
### Feeds
- "Weather": Get current weather for preconfigured location
- "Weather Forecast": Get a 5 day forecast for rain or ice
- "Word of the day": Return a word of the day with definition
- "News": Top news stories from selected sources (defined in config)
- "Thought of the day": Return random thought of the day from Reddit r/showerthoughts
- "Did you know / Teach me something": Return a random did you know from Reddit r/didyouknow
### Camera
Required: RPI Camera
- "Camera": Take photo from Raspberry Pi camera and send to user via telegram.
- "Video": Record short video from Raspberry Pi camera and send to user via telegram.
### Budgeting
- "[amount] [expense type]": Log expense of x amount of y type, convert to GBP from USD if $ included in price (e.g. '$100 tickets').
- "Budget": Show remaining monthly budget
- "Get Expenses": Download current and previous month's expenses in CSV format via telegram
### Monzo Integration
- "add monzo token <auth_code> <client_id> <client_secret>": Add a Monzo authentication for 'Get Transactions' command.
- "Get Transactions": Downloads all transactions from authenticated monzo accounts, remove expired access tokens and notify of any new transactions.
- "Get Recent Transactions": As above, but limited to the last day
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
### Property Search
- "Properties": Specific property search via Zoopla.
### Universal Translator
- "Translate <something> to <language>" - Translate a phrase to a specified language
- "Translate <something> from <language>" - Translate a phrase from a specified language to English

## Getting Started
1. `git clone https://github.com/danic85/mojo_home_bot.git`
2. Navigate to directory `mojo_home_bot`
3. `pip3 install -r requirements.txt`
4. `sudo apt-get install libav-tools` and `sudo apt-get install flac` (Required for pydub as part of speech recognition)
5. `apt-get install mongodb` to install the database

## Add Configuration Keys
Enter the command `set config <key>=<value>` for the following keys:
- Users=<user_id1>,<user_id2>
- Admin=<user_id>
- Telbot=<telegram_bot_key>
- OpenWeatherMapKey=<owm_key>
- OpenExchangeRatesKey=<open_exchange_rates_key>
- News=<source_one>,<source_two>
- NewsAPIKey=<newsapi_key>

### Execute command from the terminal
To execute a command, run `python3 main.py` and then enter the command at the prompt

### Initialize with Telegram
1. Rename the config file: `mv config.ini.example config.ini`
2. Enter the command `set config <key>=<value>` for the following keys:
  * Telbot: Telegram Bot Key https://core.telegram.org/bots (REQUIRED for telegram integration)
  * Admin: Telegram User ID (REQUIRED for telegram integration)
  * OpenWeatherMapKey: Location key from Open Weather Map
  * Users: Telegram User IDs, comma separated
  * OpenExchangeRatesKey: Key for Open Exchange Rates
  * News: Comma separated list of news sources from newsapi.org
  * NewsAPIKey: newsapi.org key
  * ZooplaAPI: API key for zoopla
3. `python3 main.py startx`

### Start on Boot
1. Add execute permission to mojo.py `chmod +x mojo.py`
2. Add `(sleep 10; python3 /home/pi/mojo_home_bot/mojo.py startx) &` to `/etc/rc.local` replacing path if appropriate.

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

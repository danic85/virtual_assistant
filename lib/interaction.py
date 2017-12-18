from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

class Interaction(object):

    def __init__(self, **kwargs):
        self.user = kwargs.get('user', None)
        self.command = kwargs.get('command', {'text': ''})
        self.response = []
        self.finish = kwargs.get('finish', True)
        self.method = kwargs.get('method', 'handle')
        self.msg = kwargs.get('msg', None)

    def respond(self, response, user=None):
        """ Add response to list """
        if user is None:
            if self.user[0] is None:
                user = self.admin
            else:
                user = self.user[0]

        if type(user) is str or type(user) is int:
            user = [user]

        print(response)

        if type(response) is dict and 'text' in response:
            if 'user' not in response:
                response['user'] = user
            self.response.append(response)
        elif type(response) is str:
            self.response.append({'text': response, 'user': user})
        else:
            raise ValueError('Response is not correct format')

    def respond_file(self, response):
        """ Add response to list """
        if type(response) is str or type(response) is unicode:
            self.response.append({'file': 'file', 'path': response})
        else:
            raise ValueError('Response is not correct format')

    def respond_keyboard(self, response):
        """ Add response to list """
        if type(response) is list:
            buttons = []
            for l in response:
                buttons.append(KeyboardButton(text=l))

            if len(buttons) == 0:
                reply_markup = ReplyKeyboardRemove(remove_keyboard=True)
            else:
                reply_markup = ReplyKeyboardMarkup(
                    keyboard=[
                        buttons
                    ]
                )

            self.response.append({'keyboard': reply_markup})
        else:
            raise ValueError('Response is not correct format')

    def respond_photo(self, response, caption=None):
        """ Add response to list """
        if type(response) is str or type(response) is unicode:
            self.response.append({'file': 'photo', 'path': response, 'caption': caption})
        else:
            raise ValueError('Response is not correct format')

    def respond_video(self, response):
        """ Add response to list """
        if type(response) is str or type(response) is unicode:
            self.response.append({'file': 'video', 'path': response})
        else:
            raise ValueError('Response is not correct format')

    def chain_command(self, command):
        """ Add response to list """
        if type(command) is dict and 'text' in command:
            if 'user' not in command:
                command['user'] = self.user
            self.response.append({'command': command})
        elif type(command) is str or type(command) is unicode:
            self.response.append({'command': {'text': command, 'user': self.user}})
        else:
            raise ValueError('Chain command is not correct format')

    def get_response_str(self):
        """ Parse all responses and return as string """
        if len(self.response) == 0:
            return ''

        r_txt = []
        for r in self.response:
            if 'text' in r and r['text'] and 'user' in r:
                r_txt.append({'text': r['text'], 'user': r['user']})

        return r_txt

    def get_response_keyboard(self):
        for r in self.response:
            if 'keyboard' in r:
                return r['keyboard']
        return None

    def get_response_files(self):
        files = []
        for r in self.response:
            if 'file' in r and r['path']:
                files.append(r)
        return files

class Interaction(object):

    def __init__(self, **kwargs):
        self.user = kwargs.get('user', None)
        self.command = kwargs.get('command', {'text': ''})
        self.response = []
        self.finish = kwargs.get('finish', True)
        self.method = kwargs.get('method', 'handle')
        self.msg = kwargs.get('msg', None)

    def respond(self, response):
        """ Add response to list """
        if type(response) is dict and 'text' in response:
            self.response.append(response)
        elif type(response) is str or type(response) is unicode:
            self.response.append({'text': response})
        else:
            raise ValueError('Response is not correct format')

    def respond_file(self, response):
        """ Add response to list """
        if type(response) is str or type(response) is unicode:
            self.response.append({'file': 'file', 'path': response})
        else:
            raise ValueError('Response is not correct format')

    def respond_photo(self, response):
        """ Add response to list """
        if type(response) is str or type(response) is unicode:
            self.response.append({'file': 'photo', 'path': response})
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
            self.response.append({'command': command})
        elif type(command) is str or type(command) is unicode:
            self.response.append({'command': {'text': command}})
        else:
            raise ValueError('Chain command is not correct format')

    def get_response_str(self):
        """ Parse all responses and return as string """
        if len(self.response) == 0:
            return ''

        r_txt = []
        for r in self.response:
            if 'text' in r and r['text']:
                r_txt.append(r['text'])

        return '\n'.join(r_txt)

    def get_response_files(self):
        files = []
        for r in self.response:
            if 'file' in r and r['path']:
                files.append(r)
        return files

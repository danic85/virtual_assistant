import telepot


class Telegram(telepot.Bot):
    def __init__(self, **kwargs):
        self.config = kwargs.get('config', None)
        super(Telegram, self).__init__(self.config.get_or_request('Telbot'))

    def admin_message(self, msg):
        if msg == '':
            return

        self.sendMessage(self.config.get_or_request('Admin'), msg)

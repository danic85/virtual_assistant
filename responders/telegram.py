import telepot
import urllib
from pydub import AudioSegment
import lib

class Telegram(telepot.Bot):
    def __init__(self, **kwargs):
        self.config = kwargs.get('config', None)
        self.files = kwargs.get('files', None)
        super(Telegram, self).__init__(self.config.get_or_request('Telbot'))

    def get_text(self, msg):
        if 'chat' not in msg or 'id' not in msg['chat']:
            self.admin_message('Could not find user for : ' + str(msg['text']))
            return

        if str(msg['chat']['id']) not in self.config.get_or_request('Users').split(','):
            self.admin_message('Unauthorized access attempt by: ' + str(msg['chat']['id']))
            return

        if 'voice' in msg:
            msg['text'] = self.recognise_voice(msg)

        if 'text' not in msg:
            return ''

        return msg['text']

    def admin_message(self, msg):
        if msg == '':
            return

        self.sendMessage(self.config.get_or_request('Admin'), msg)

    def recognise_voice(self, msg):
        fpath = self.files + '/speech/input'  # includes filename without extension
        f = self.getFile(msg['voice']['file_id'])
        filepath = 'https://api.telegram.org/file/bot' + self.config.get('Telbot') + '/' + str(f['file_path'])
        self.logging.info(filepath)

        # Retrieve from URL and save to files
        urllib.urlretrieve(filepath, fpath + '.oga')

        # convert form OGG to WAV
        ogg_version = AudioSegment.from_ogg(fpath + '.oga')
        ogg_version.export(fpath + '.wav', format="wav")

        return lib.speech.recognise(fpath + '.wav')
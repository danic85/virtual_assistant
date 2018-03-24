import telepot
import urllib
from pydub import AudioSegment
import lib
import os
# from gtts import gTTS
import urllib
import speech_recognition as sr
import _thread

class Telegram(telepot.Bot):
    def __init__(self, **kwargs):
        self.config = kwargs.get('config', None)
        self.files = kwargs.get('files', None)
        self.logging = kwargs.get('logging', None)
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
        self.logging.info('Retrieving from URL')
        urllib.request.urlretrieve(filepath, fpath + '.oga')

        self.logging.info('Convert to WAV')
        # convert form OGG to WAV
        ogg_version = AudioSegment.from_ogg(fpath + '.oga')
        ogg_version.export(fpath + '.wav', format="wav")

        return self.recognise(fpath + '.wav')

    def recognise(self, wavpath):
        audio = None
        try:
            # Recognize audio
            self.logging.info('Recognizing...')
            r = sr.Recognizer()
            with sr.AudioFile(wavpath) as source:
                audio = r.record(source)  # read the entire audio file

        except Exception as ex:
            return str(ex)

        self.logging.info('Removing File')
        _thread.start_new_thread(os.remove, (wavpath,))

        command = ''

        # recognize speech using Sphinx
        try:
            command = r.recognize_sphinx(audio)
            self.logging.info("Sphinx thinks you said " + command)
        except sr.UnknownValueError:
            self.logging.info("Sphinx could not understand audio")
        except sr.RequestError as e:
            self.logging.info("Sphinx error; {0}".format(e))
        return command
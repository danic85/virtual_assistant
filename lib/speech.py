#!/usr/bin/python
# -*- coding: latin-1 -*-


try:
    from gtts import gTTS
    import urllib
    import speech_recognition as sr
    from pydub import AudioSegment
except ImportError as e:
    print str(e)


def speak(self, response):
    tts = gTTS(text=response, lang='en')
    tts.save(self.files + '/speech/output.mp3')


def getMessage(self, msg):
    try:
        command = 'voice received'
        fpath = self.files + '/speech/input'  # includes filename without extension
        f = self.getFile(msg['voice']['file_id'])
        filepath = 'https://api.telegram.org/file/bot' + self.config.get('Config', 'Telbot') + '/' + str(f['file_path'])
        self.logging.info(filepath)

        # Retrieve from URL and save to files
        urllib.urlretrieve(filepath, fpath + '.oga')

        # convert form OGG to WAV
        ogg_version = AudioSegment.from_ogg(fpath + '.oga')
        ogg_version.export(fpath + '.wav', format="wav")

        # Recognize audio
        r = sr.Recognizer()
        with sr.AudioFile(fpath + '.wav') as source:
            audio = r.record(source)  # read the entire audio file
    except Exception as e:
        return e.getMessage();

    # @todo configure Sphinx with https://pypi.python.org/pypi/SpeechRecognition/
    # recognize speech using Sphinx
    # try:
    #   print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    # except sr.UnknownValueError:
    #   print("Sphinx could not understand audio")
    # except sr.RequestError as e:
    #   print("Sphinx error; {0}".format(e))

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        command = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + command)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return command

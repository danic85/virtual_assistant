#!/usr/bin/python
# -*- coding: latin-1 -*-
import os

try:
    from gtts import gTTS
    import urllib
    import speech_recognition as sr

except ImportError as e:
    print (str(e))


def speak(self, response):
    tts = gTTS(text=response, lang='en')
    tts.save(self.files + '/speech/output.mp3')


def recognise(wavpath):
    try:
        # Recognize audio
        r = sr.Recognizer()
        with sr.AudioFile(wavpath) as source:
            audio = r.record(source)  # read the entire audio file

    except Exception as ex:
        return str(ex)

    os.remove(wavpath)

    command = ''

    # recognize speech using Sphinx
    try:
        command = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + command)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return command




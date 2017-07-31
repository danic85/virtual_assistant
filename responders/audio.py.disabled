import pyaudio
import wave
import audioop
from collections import deque
import time
import math
from lib import speech
from responders.console import Console
import pygame
from pydub import AudioSegment
import os


""" https://github.com/jeysonmc/python-google-speech-scripts/blob/master/stt_google.py """

LANG_CODE = 'en-US'  # Language to use

GOOGLE_SPEECH_URL = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&pfilter=2&lang=%s&maxresults=6' % (LANG_CODE)

FLAC_CONV = 'flac -f'  # We need a WAV to FLAC converter. flac is available
                       # on Linux

# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 3000  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 1  # Silence limit in seconds. The max amount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.

PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.


class Audio(Console):

    def __init__(self, **kwargs):
        self.config = kwargs.get('config', None)
        self.files = kwargs.get('files', None)
        self.callback = None
        self.threshold = self.audio_int() + 800

    @staticmethod
    def get_text(msg):
        if 'voice' in msg:
            msg['text'] = speech.recognise(msg['voice']['file_id'])
            if 'mojo' not in msg['text']:
                return ''

        if 'text' not in msg:
            return ''
        return msg['text']

    def sendAudio(self, user, path):
        sound = AudioSegment.from_mp3(path)
        sound.export(path[:-4]+'.wav', format="wav")

        os.remove(path)

        pygame.mixer.init()
        pygame.mixer.music.load(path[:-4]+'.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        os.remove(path[:-4]+'.wav')

    def audio_int(self, num_samples=50):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the 20% largest intensities recorded.
        """

        print("Getting intensity values from mic.")
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print(" Finished ")
        print(" Average audio intensity is ", r)
        stream.close()
        p.terminate()
        return r

    def message_loop(self, callback):
        """
        Listens to Microphone, extracts phrases from it and sends it to
        Google's TTS service and returns response. a "phrase" is sound
        surrounded by silence (according to threshold). num_phrases controls
        how many phrases to process before finishing the listening process
        (-1 for infinite).
        """

        num_phrases = 1
        #Open stream
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* Listening mic. ")
        audio2send = []
        cur_data = ''  # current chunk  of audio data
        rel = RATE/CHUNK
        slid_win = deque(maxlen=int(SILENCE_LIMIT * rel))
        #Prepend audio from 0.5 seconds before noise was detected
        prev_audio = deque(maxlen=int(PREV_AUDIO * rel))
        started = False
        n = num_phrases
        response = []

        while (num_phrases == -1 or n > 0):
            cur_data = stream.read(CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            #print slid_win[-1]
            if(sum([x > self.threshold for x in slid_win]) > 0):
                if(not started):
                    print("Starting record of phrase")
                    started = True
                audio2send.append(cur_data)
            elif (started is True):
                print("Finished")
                # The limit was reached, finish capture and deliver.
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                # Send file to Google and get response
                # r = self.stt_google_wav(filename)
                # # r = speech.recognise(os.path.dirname(os.path.realpath(__file__)) + '/' + filename)
                # if num_phrases == -1:
                #     print "Response", r
                # else:
                #     response.append(r)
                # # Remove temp file. Comment line to review.
                # os.remove(filename)
                # Reset all
                started = False
                slid_win = deque(maxlen=int(SILENCE_LIMIT * rel))
                prev_audio = deque(maxlen=int(0.5 * rel))
                audio2send = []
                n -= 1
                print("Listening ...")
            else:
                prev_audio.append(cur_data)

        print("* Done recording")
        stream.close()
        p.terminate()

        callback({"chat": {"id": 0}, "voice": {"file_id": filename}})

    def save_speech(self, data, p):
        """ Saves mic data to temporary WAV file. Returns filename of saved
            file """

        filename = self.files + '/speech/output_'+str(int(time.time()))
        # writes data to WAV file
        data = b''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)  # TODO make this value a function parameter?
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

import time
import sys
import threading

class Console(object):
    def __init__(self, **kwargs):
        self.config = kwargs.get('config', None)
        self.callback = None

    @staticmethod
    def get_text(msg):
        if 'text' not in msg:
            return ''
        return msg['text']

    def admin_message(self, msg):
        if msg == '':
            return

        self.sendMessage(self.config.get_or_request('Admin'), msg)

    def sendMessage(self, user, msg,
                    parse_mode=None, disable_web_page_preview=None,
                    disable_notification=None, reply_to_message_id=None, reply_markup=None):
        print(msg)

    def sendPhoto(self, user, file, caption):
        self.sendMessage(user, 'sendPhoto not supported in console mode')
        self.sendMessage(user, caption)

    def sendDocument(self, user, file):
        self.sendMessage(user, 'sendDocument not supported in console mode')

    def sendVideo(self, user, file):
        self.sendMessage(user, 'sendVideo not supported in console mode')

    def sendAudio(self, user, file):
        self.sendMessage(user, 'sendAudio not supported in console mode')

    def message_loop(self, callback):
        self.callback = callback
        """ Allow threaded message loop. @todo handle threading - currently only runs once """
        if sys.version_info < (3, 0):  # pragma: no cover
            command = raw_input("Enter command: ")
        else:
            command = input("Enter command: ")

        if self.callback is not None:
            self.callback({"chat": {"id": 0}, "text": command})

    # def message_loop(self, callback):
    #     self.callback = callback
    #     def get_from_input():
    #         while 1:
    #             """ Allow threaded message loop. @todo handle threading - currently only runs once """
    #             if sys.version_info < (3, 0):  # pragma: no cover
    #                 command = raw_input("Enter command: ")
    #             else:
    #                 command = input("Enter command: ")
    #
    #             if self.callback is not None:
    #                 self.callback({"chat": {"id": self.config.get_or_request('Admin')}, "text": command})
    #             time.sleep(10)
    #
    #     t = threading.Thread(target=get_from_input)
    #
    #     t.daemon = True  # need this for main thread to be killable by Ctrl-C
    #     t.start()





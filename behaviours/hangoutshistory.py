import json
import os
import time, datetime

path = os.path.dirname(os.path.realpath(__file__)) + '/../files/hangouts-export.json'
with open(path) as data_file:
    data = json.load(data_file)

for conversation in data['conversation_state']:

    last_time = ''
    if 'conversation' in conversation['conversation_state']:
        participants = {}
        if 'participant_data' in conversation['conversation_state']['conversation']:
            for participant in conversation['conversation_state']['conversation']['participant_data']:
                if 'fallback_name' not in participant:
                    participant['fallback_name'] = 'Unknown'
                participants[participant['id']['chat_id']] = participant['fallback_name']
    for event in conversation['conversation_state']['event']:
        if 'chat_message' in event and 'message_content' in event['chat_message']:
            if 'segment' in event['chat_message']['message_content']:
                for segment in event['chat_message']['message_content']['segment']:
                    if 'text' in segment and str(segment['text'].encode('utf-8')).strip() != '':
                        t = time.strftime("%d/%m/%Y %H:%M", time.gmtime(int(event['timestamp'])/1000000))
                        if t != last_time:
                            print t
                            last_time = t
                        if event['sender_id']['chat_id'] in participants:
                            print participants[event['sender_id']['chat_id']] + ': ' + segment['text']
                        else:
                            print segment['text']
    print '-----------'
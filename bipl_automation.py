from flask import Flask, request, jsonify
import threading
import datetime
import re
from slack_sdk import WebClient
app = Flask(__name__)
from slack_sdk.errors import SlackApiError
from sheet import *
slack_bot_token = 'token_comes_here'
slack_client = WebClient(token=slack_bot_token)
@app.route('/slack/bipl/', methods=['POST', 'GET'])
def handle_slack_event():
    payload = request.json
    thread = threading.Thread(target=Test, args=(payload,))
    thread.start()
 #   print(thread)
    return 'OK'


def Test(payload):

#    print(payload)
    if 'event' in payload and 'type' in payload['event'] and payload['event']['type'] == 'message':
        event = payload['event']
        thread = payload['event']['ts']
#        print(thread)
#        print(payload['event'])
        text = event['text']
   #     print(text)
        if 'Shift Clients Assignment' in text:
          text = text.replace('Shift Clients Assignment submission from', '')
          print("text is :", text)
          shift = extract_info(text, '*Shift*', '*Shift Lead*')
          analyst_name=extract_info(text, '*BIPL*', '*VeeOne*')
          print('Shift is :', shift)
          print(' and Analyst name is :', analyst_name)
          analyst_name = get_user_email(analyst_name)
          date = extract_date_from_slack_message(slack_client, event)
        #  print('Shift is :', shift)
          print('Analyst name is :', analyst_name)
          #print('Date is:', date)
          date_parts = date.split(" ")[0]
          print("DATE PART ", date_parts)
          if analyst_name == "Unknown Email":
             return
          variable=find_cell(date_parts,shift,analyst_name)
          if variable == 1:
            print(variable)
            send_reply_excuses(thread,f"Name : {analyst_name} for date: {date_parts} is added in the BIPL Onshift Sheet")
          else:
            send_reply_excuses(thread,f"Error: Sheet is not updated, Kindly edit sheet manually")
        else:
          print("randome text")

def send_reply_excuses(thread, Text):
    channel_id = "C04C2LAPAUR"
    try:
       result = slack_client.chat_postMessage(channel=channel_id, text=Text, thread_ts = thread)

    except SlackApiError as e:
       print(f"Error fetching the message from Slack: {e.response['error']}")

def extract_info(text, start_marker, end_marker):
    start_index = text.find(start_marker) + len(start_marker)
    end_index = text.find(end_marker, start_index)
    return text[start_index:end_index].strip()

def extract_date_from_slack_message(slack_client, event):
    channel_id = event['channel']
    timestamp = event['ts']

    # Get the Slack message from the channel
    try:
        message = slack_client.conversations_history(channel=channel_id, latest=timestamp, limit=1)
        if message['ok'] and 'messages' in message and len(message['messages']) > 0:
            message_date = float(message['messages'][0]['ts'])
            return datetime.datetime.fromtimestamp(message_date).strftime('%Y-%m-%d %H:%M:%S')
    except SlackApiError as e:
        print(f"Error fetching the message from Slack: {e.response['error']}")

    return None

 #.............. extract user name from slack....................
def get_user_email(analyst_name):
    try:
        user_id = analyst_name.strip('*<@>')
        print("troubleshooting email is :", analyst_name)
        response = slack_client.users_info(user=user_id, include_locale=True)
        user_info = response['user']
        email = user_info.get('profile', {}).get('email')
        if email:
            username = email.split("@")[0]
            return username
        else:
            return 'Email not available'
    except Exception as e:
        print(f"Failed to retrieve email for user ID {user_id}: {str(e)}")
        return 'Unknown Email'



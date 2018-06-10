from adelita import question_order, opening_script_question, Profile, permission_to_talk_text
import os
import time
import re
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 5 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "Register"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


if __name__ == "__main__":

    collected_data = {
        'name': None,
        'zipcode': None,
        'email': None,
        'phone_number': None,
        'interests': None,
        'notes': None
    }

    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())

            if command and command.startswith(EXAMPLE_COMMAND):
                response = "Sure... let's get started!"

                slack_client.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text=response
                )

                slack_client.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text=opening_script_question.text[0]
                )

            if command and command.startswith(EXAMPLE_COMMAND):

                for question in question_order:

                    for indx, text in enumerate(question.text):
                        if question.format and question.format[indx]:
                            text = text.format(collected_data[question.format[indx]])

                        slack_client.api_call(
                            "chat.postMessage",
                            channel=channel,
                            text=text
                        )

                        if '?' in text:
                            if question.options:
                                text = 'Options:\n'
                                for option in question.options:
                                    text += '{}\n'.format(option)

                                time.sleep(5.0)
                                slack_client.api_call(
                                    "chat.postMessage",
                                    channel=channel,
                                    text=text
                                )

                            if collected_data.get(question.data):
                                collected_data[question.data] = command
                        time.sleep(5.0)
                        if command == "quit" or command == "bye":

                            break

            user_profile = Profile(**collected_data)
            print(user_profile)


            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
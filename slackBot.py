import logging, config
from slack import WebClient
from slack.errors import SlackApiError

client = WebClient(token=config.SLACK_TOKEN)
logger = logging.getLogger(__name__)

def post_message(message, channel_id):
    try:
        result = client.chat_postMessage(
            channel=channel_id,
            text = message
        )

    except SlackApiError as e:
        print("Error: {e}")

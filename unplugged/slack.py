"""Hardcoded to tag Gunnar in messages"""

from dotenv import dotenv_values
import requests

HEADERS = {'Content-type': 'application/json'}


config: dict[str, str] = dotenv_values('.env')
URL: str = config['URL']
USER_ID: str = config['USER_ID']


def _prepare_message(message: str) -> dict:
    """Messages must be dictionaries.
    
    Args:
        message (str): The message to be sent to channel.

    Returns:
        dict: Formatted text ready to be sent to channel.
    """
    return {'text': message}


def _prepend_user_id(message: str) -> str:
    """Formats message appropriately to tag user.
    
    Args:
        message (str): The message to be sent to channel.
        user_id (str): User ID for tagging user in message.
            Refer to Notion manual on how to find.
    """
    return f'<@{USER_ID}>\n {message}'


def post(message: str) -> requests.Response:
    """Sends message to slack channel.

    Requires incoming webhooks enabled for the channel IDd
    by the url. 
    
    Args:
        message (str): The message to be sent to channel.
        url (str): Unique channel URL as generated when
            the webhook was enabled. Be careful not to
            share this externally.
        user_id (str): User ID for tagging user in message.
            Refer to Notion manual on how to find.
    """

    message_: str = _prepend_user_id(message=message)
    outgoing_message: dict[str, str] = _prepare_message(message=message_)
    
    return requests.post(url=URL, headers=HEADERS, json=outgoing_message)
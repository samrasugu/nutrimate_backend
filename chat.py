import boto3
import os

# Load env variables
aws_region = os.environ['AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
locale = os.environ['LOCALE']
session_id = os.environ['SESSION_ID']
bot_id = os.environ['BOT_ID']
bot_alias_id = os.environ['BOT_ALIAS_ID']
client = boto3.client('lex-runtime')

class BotClient:
    def __init__(self):
        self.client = client
        self.locale = locale
        self.session_id = session_id
        self.bot_id = bot_id
        self.bot_alias_id = bot_alias_id
    
    def recognize_text(self, message):
        response = self.client.recognize_text(
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId=locale,
            sessionId=session_id,
            text=message
        )
        return response
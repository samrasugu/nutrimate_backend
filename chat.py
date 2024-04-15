import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Load env variables
aws_region = os.getenv('AWS_REGION')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
locale = os.getenv('LOCALE')
session_id = os.getenv('SESSION_ID')
bot_id = os.getenv('BOT_ID')
bot_alias_id = os.getenv('BOT_ALIAS_ID')
client = boto3.client('lex-runtime', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

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
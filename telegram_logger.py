import requests
import traceback

class TelegramErrorLogger:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, text):
        """Send a message to the Telegram chat"""
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(self.base_url, data=payload)
            return response.json()
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")

    def log_error(self, error):
        """Format and send an error message"""
        error_traceback = traceback.format_exc()
        message = (
            f"🚨 <b>Error occurred</b> 🚨\n"
            f"<pre>{error}</pre>\n"
            f"<b>Traceback:</b>\n"
            f"<pre>{error_traceback}</pre>"
        )
        self.send_message(message)
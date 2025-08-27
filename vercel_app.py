import os
from flask import Flask, request
import telegram

TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # Process your update (e.g., reply to messages)
    chat_id = update.message.chat.id
    message = update.message.text
    bot.send_message(chat_id=chat_id, text=f"You said: {message}")
    return "ok"

# (Optional) Route to set webhook if you want to do it from your app
@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    webhook_url = os.environ['WEBHOOK_URL']
    s = bot.set_webhook(webhook_url + '/webhook')
    return "webhook setup: " + str(s)

import os
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application

from bot import TelegramBot  # Import your bot logic

app = Flask(__name__)

# Create your bot instance ONCE
telegram_bot = TelegramBot()
application = telegram_bot.application

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    try:
        application.process_update(update)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return "ok", 200

@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    webhook_url = os.environ.get('WEBHOOK_URL', '')
    success = application.bot.set_webhook(webhook_url + '/webhook')
    return "webhook setup: " + str(success)

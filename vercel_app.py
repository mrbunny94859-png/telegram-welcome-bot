import os
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application

# Import your TelegramBot class!
from bot import TelegramBot

app = Flask(__name__)

# Create your bot instance (make sure to use the correct token env var)
telegram_bot = TelegramBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get update from Telegram
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_bot.application.bot)
    
    # Process update using your bot's handlers
    # For python-telegram-bot v20+, you need to call process_update
    try:
        telegram_bot.application.process_update(update)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return "ok", 200

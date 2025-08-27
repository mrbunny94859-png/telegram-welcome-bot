import threading
import time
import logging
import os
from flask import Flask
import json

logger = logging.getLogger(__name__)

# Flask app for keeping the bot alive
app = Flask('')

@app.route('/')
def home():
    """Main status page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 M.O.M Bot - 24/7 Active</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                max-width: 700px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
                border: 1px solid rgba(255, 255, 255, 0.18);
                text-align: center;
                width: 100%;
            }
            .status {
                font-size: 28px;
                margin-bottom: 30px;
                font-weight: bold;
            }
            .emoji {
                font-size: 48px;
                margin: 20px 0;
            }
            .info {
                margin: 15px 0;
                font-size: 18px;
                opacity: 0.9;
            }
            .commands {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
            }
            .commands h3 {
                margin-top: 0;
                color: #ffd700;
            }
            .command {
                margin: 8px 0;
                font-family: 'Courier New', monospace;
                font-size: 16px;
            }
            .footer {
                margin-top: 30px;
                font-size: 14px;
                opacity: 0.7;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🤖💰</div>
            <div class="status">M.O.M Bot is ACTIVE!</div>
            <div class="info">🔥 <strong>Status:</strong> Running 24/7</div>
            <div class="info">🚀 <strong>Service:</strong> Bitcoin Transaction Cancellation Bot</div>
            <div class="info">⚡ <strong>Version:</strong> 3.0.0</div>
            <div class="info">🌐 <strong>Uptime:</strong> Continuous</div>
            
            <div class="commands">
                <h3>📋 Available Commands:</h3>
                <div class="command">💼 /work - Project Information</div>
                <div class="command">📖 /manual - BTC Transaction Guides</div>
                <div class="command">👑 /teamlead - Contact Boss</div>
                <div class="command">⚙️ /admin - Admin Functions</div>
            </div>
            
            <div class="footer">
                Bot is successfully running and ready for crew members! 🔥
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """JSON health check endpoint."""
    return {
        "status": "healthy",
        "service": "M.O.M-telegram-bot",
        "version": "3.0.0",
        "uptime": True,
        "timestamp": time.time(),
        "message": "Bot is running 24/7!"
    }

@app.route('/status')
def status():
    """Simple status endpoint."""
    return "Bot is running! 🤖"

def run_flask():
    """Run Flask server."""
    port = int(os.getenv("PORT", "8080"))
    app.run(host='0.0.0.0', port=port, debug=False)

def keep_alive():
    """Start the Flask keep-alive server in a separate thread."""
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()
    logger.info("🌐 Flask keep-alive server started on http://0.0.0.0:8080")
    logger.info("✅ Keep-alive service activated")

# Additional monitoring function
def monitor_bot():
    """Monitor bot health and log status periodically."""
    def monitor_loop():
        while True:
            try:
                logger.info("🔍 Bot health check - Running normally")
                time.sleep(300)  # Check every 5 minutes
            except Exception as e:
                logger.error(f"Health check error: {e}")
                time.sleep(60)  # Retry in 1 minute on error
    
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    logger.info("📊 Health monitoring activated")

if __name__ == "__main__":
    keep_alive()
    monitor_bot()
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keep-alive server stopped")

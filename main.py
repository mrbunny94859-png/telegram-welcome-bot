import os
import asyncio
import logging
import signal
import sys
from bot import TelegramBot
from keep_alive import keep_alive

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

class BotManager:
    def __init__(self):
        self.bot = None
        self.running = False
        self.restart_count = 0
        self.max_restarts = 10

    async def start_bot(self):
        """Start the Telegram bot with error handling and restart logic."""
        while self.restart_count < self.max_restarts:
            try:
                logger.info(f"Starting bot (attempt {self.restart_count + 1})")
                self.bot = TelegramBot()
                self.running = True
                await self.bot.start()
                break
            except Exception as e:
                self.restart_count += 1
                logger.error(f"Bot crashed (attempt {self.restart_count}): {e}")
                if self.restart_count >= self.max_restarts:
                    logger.critical("Max restart attempts reached. Exiting.")
                    sys.exit(1)
                await asyncio.sleep(10)  # Wait before restart

    async def stop_bot(self):
        """Stop the bot gracefully."""
        if self.bot and self.running:
            logger.info("Stopping bot gracefully...")
            self.running = False
            await self.bot.stop()

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}. Shutting down...")
    asyncio.create_task(bot_manager.stop_bot())

# Global bot manager instance
bot_manager = BotManager()

async def main():
    """Main entry point for the bot."""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the keep-alive server
    keep_alive()

    # Start the bot
    try:
        await bot_manager.start_bot()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
    finally:
        await bot_manager.stop_bot()

if __name__ == "__main__":
    logger.info("🤖 Starting Telegram Bot Manager...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        sys.exit(1)

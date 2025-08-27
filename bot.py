import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import NetworkError, TimedOut, BadRequest

# Configure logging
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        # Get bot token from environment variable
        self.bot_token = os.getenv("BOT_TOKEN", "")
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable is required")
        
        self.application = None
        self.running = False
        
        # Admin users (add your user ID here)
        self.admin_users = [5839648321]
        
        # Bot content and responses
        self.bot_content = {
            "welcome": """✅ You're IN, bro! 🔥

Let's get this bread! 💰

You're now part of our exclusive crew, all features unlocked! 🚀

🔻 QUICK START GUIDE 🔻

First things first, understand what we do here:
👉 /work

Master the BTC transaction reversal game with our guide:
👉 /manual

After studying everything, practice the reversal methods with your own wallets.

Got questions? Hit up the boss:
👉 /teamlead

Studied? Practiced? Ready to make bank? Message the team lead:
👉 /teamlead

All commands and menu are now live for you!
👇 CHECK OUT THE COMMANDS""",
            
            "work": """💼 **Project Buzz:**
 [**CHECK IT OUT**](https://telegra.ph/MOM-WORK-MANUAL-08-27)""",
            
            "manual": """ **Manual for cancelling BTC transaction from PC:**
💻 [**CLICK HERE**](https://telegra.ph/MANUAL-CANCEL-BITCOIN-TRANSACTION-08-27)

 **Manual for cancelling BTC transaction from your phone:**
📲 [**CLICK HERE**](https://telegra.ph/P2P-SCAM--Cancel-BTC-transaction-instruction-for-phone-08-27)""",
            
            "teamlead": """🚀 **THE BOSS:** 🚀
👑 [**CONTACT NOW**](https://t.me/bunny2322)"""
        }

        # Help content in HTML with hidden links
        self.bot_content["help"] = (
            "🤖 <b>Quick Links</b><br/><br/>"
            "❓ Any questions? <a href=\"https://t.me/bunny2322\">TeamLead</a><br/>"
            "📚 Work details: <a href=\"https://telegra.ph/MOM-WORK-MANUAL-08-27\">Work Manual</a><br/>"
            "🧠 BTC cancel guides: <a href=\"https://telegra.ph/MANUAL-CANCEL-BITCOIN-TRANSACTION-08-27\">PC Manual</a> | "
            '<a href="https://telegra.ph/P2P-SCAM--Cancel-BTC-transaction-instruction-for-phone-08-27">Phone Manual</a><br/>'
            "💸 See team earnings: <a href=\"https://t.me/+jLaT5__nD29hYjFl\">Workers Profits</a><br/><br/>"
            "📢 Join the channel for more info & updates: <a href=\"https://t.me/+jLaT5__nD29hYjFl\">M.O.M | Info</a>"
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        try:
            user_id = update.effective_user.id
            username = update.effective_user.username or "Unknown"
            
            # Store user info for broadcasting (simple in-memory storage)
            if not hasattr(self, 'user_database'):
                self.user_database = set()
            self.user_database.add(user_id)
            
            await update.message.reply_text(
                self.bot_content['welcome']
            )
            logger.info(f"Start command executed for user {username} ({user_id})")
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await self.send_error_message(update, "Failed to process start command")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send help information."""
        try:
            keyboard = [
                [InlineKeyboardButton(text="TeamLead", url="https://t.me/bunny2322")],
                [InlineKeyboardButton(text="Work Manual", url="https://telegra.ph/MOM-WORK-MANUAL-08-27")],
                [
                    InlineKeyboardButton(text="PC Manual", url="https://telegra.ph/MANUAL-CANCEL-BITCOIN-TRANSACTION-08-27"),
                    InlineKeyboardButton(text="Phone Manual", url="https://telegra.ph/P2P-SCAM--Cancel-BTC-transaction-instruction-for-phone-08-27"),
                ],
                [InlineKeyboardButton(text="Workers Profits", url="https://t.me/+jLaT5__nD29hYjFl")],
                [InlineKeyboardButton(text="M.O.M | Info (Channel)", url="https://t.me/+jLaT5__nD29hYjFl")],
            ]
            markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Quick links:",
                reply_markup=markup,
                disable_web_page_preview=True,
            )
            logger.info(f"Help command executed for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await self.send_error_message(update, "Failed to process help command")

    async def manual_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send manual with Telegraph links."""
        try:
            await update.message.reply_text(
                self.bot_content['manual'],
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            logger.info(f"Manual command executed for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in manual command: {e}")
            await self.send_error_message(update, "Failed to process manual command")

    async def docs_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send documentation links."""
        try:
            await update.message.reply_html(self.bot_content['help'], disable_web_page_preview=True)
            logger.info(f"Docs command executed for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in docs command: {e}")
            await self.send_error_message(update, "Failed to process docs command")

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send bot information."""
        try:
            await update.message.reply_markdown_v2(self.bot_content['info'])
            logger.info(f"Info command executed for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in info command: {e}")
            await self.send_error_message(update, "Failed to process info command")

    async def work_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send work information."""
        try:
            await update.message.reply_text(
                self.bot_content['work'],
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            logger.info(f"Work command executed for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in work command: {e}")
            await self.send_error_message(update, "Failed to process work command")

    async def teamlead_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send team lead information."""
        try:
            await update.message.reply_text(
                self.bot_content['teamlead'],
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            logger.info(f"Teamlead command executed for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in teamlead command: {e}")
            await self.send_error_message(update, "Failed to process teamlead command")

    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Admin command for sending custom messages."""
        try:
            if update.effective_user.id not in self.admin_users:
                await update.message.reply_text("❌ Access denied. Admin only.")
                return
                
            if not context.args or len(context.args) < 2:
                await update.message.reply_text(
                    "Usage:\n"
                    "📤 /admin <user_id> <message> - Send to specific user\n"
                    "📢 /admin broadcast <message> - Send to all users\n\n"
                    "Examples:\n"
                    "• /admin 123456789 Hello from admin!\n"
                    "• /admin broadcast Important announcement!"
                )
                return
                
            if context.args[0] == "broadcast":
                message = " ".join(context.args[1:])
                await self.broadcast_to_all_users(update, message)
            else:
                user_id = int(context.args[0])
                message = " ".join(context.args[1:])
                
                success = await self.send_custom_message(user_id, message)
                if success:
                    await update.message.reply_text(f"✅ Message sent to user {user_id}")
                else:
                    await update.message.reply_text(f"❌ Failed to send message to user {user_id}")
                
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID. Must be a number.")
        except Exception as e:
            logger.error(f"Error in admin command: {e}")
            await update.message.reply_text("❌ Error processing admin command.")

    async def broadcast_to_all_users(self, update: Update, message: str) -> None:
        """Broadcast message to all users who have used the bot."""
        try:
            if not hasattr(self, 'user_database') or not self.user_database:
                await update.message.reply_text("❌ No users found in database.")
                return
                
            await update.message.reply_text(f"📢 Broadcasting to {len(self.user_database)} users...")
            
            success_count = 0
            failed_count = 0
            
            for user_id in self.user_database:
                success = await self.send_custom_message(user_id, message)
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    
            await update.message.reply_text(
                f"📊 **Broadcast Results:**\n"
                f"✅ Successfully sent: {success_count}\n"
                f"❌ Failed: {failed_count}\n"
                f"👥 Total users: {len(self.user_database)}"
            )
            
        except Exception as e:
            logger.error(f"Error in broadcast: {e}")
            await update.message.reply_text("❌ Error during broadcast.")

    async def send_custom_message(self, user_id: int, message: str) -> bool:
        """Send a custom message to a specific user."""
        try:
            await self.application.bot.send_message(
                chat_id=user_id,
                text=message
            )
            logger.info(f"Custom message sent to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending custom message to user {user_id}: {e}")
            return False

    async def broadcast_message(self, message: str, user_ids: list = None) -> dict:
        """Broadcast a message to multiple users."""
        results = {"success": [], "failed": []}
        
        if user_ids is None:
            logger.warning("No user IDs provided for broadcast")
            return results
            
        for user_id in user_ids:
            success = await self.send_custom_message(user_id, message)
            if success:
                results["success"].append(user_id)
            else:
                results["failed"].append(user_id)
                
        logger.info(f"Broadcast completed: {len(results['success'])} successful, {len(results['failed'])} failed")
        return results

    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle unknown commands."""
        try:
            await update.message.reply_text(
                "❓ Unknown command. Use /help to see available commands."
            )
            logger.info(f"Unknown command from user {update.effective_user.id}: {update.message.text}")
        except Exception as e:
            logger.error(f"Error in unknown command handler: {e}")

    async def send_error_message(self, update: Update, error_msg: str) -> None:
        """Send a user-friendly error message."""
        try:
            await update.message.reply_text(
                f"❌ {error_msg}. Please try again later or contact support."
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the user."""
        logger.error(f"Exception while handling an update: {context.error}")
        
        if isinstance(context.error, (NetworkError, TimedOut)):
            logger.warning("Network error occurred, bot will retry")
            return
            
        if isinstance(update, Update) and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "❌ Sorry, something went wrong. Please try again."
                )
            except Exception as e:
                logger.error(f"Failed to send error notification: {e}")

    async def callback_query_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle callback queries from inline keyboards."""
        try:
            query = update.callback_query
            await query.answer()
            
            if query.data == "help":
                await query.edit_message_text(
                    text=self.bot_content['help'],
                    parse_mode='MarkdownV2'
                )
                logger.info(f"Callback query 'help' processed for user {query.from_user.id}")
        except Exception as e:
            logger.error(f"Error in callback query handler: {e}")

    def setup_handlers(self):
        """Set up all command and message handlers."""
        if not self.application:
            return
            
        # Register command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("docs", self.docs_command))
        self.application.add_handler(CommandHandler("work", self.work_command))
        self.application.add_handler(CommandHandler("manual", self.manual_command))
        self.application.add_handler(CommandHandler("teamlead", self.teamlead_command))
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        
        # Handle unknown commands
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_command))
        
        # Add error handler
        self.application.add_error_handler(self.error_handler)

    async def set_bot_commands(self) -> None:
        """Register slash commands so clients show suggestions when typing '/'."""
        try:
            commands = [
                BotCommand(command="start", description="Start and get welcome info"),
                BotCommand(command="help", description="Help and quick links"),
                BotCommand(command="work", description="Project info"),
                BotCommand(command="manual", description="BTC cancel manuals"),
                BotCommand(command="teamlead", description="Contact team lead"),
            ]

            await self.application.bot.set_my_commands(commands)
            logger.info("✅ Bot commands registered")
        except Exception as e:
            logger.error(f"Failed to set bot commands: {e}")

    async def start(self):
        """Start the bot."""
        try:
            # Create the Application
            self.application = Application.builder().token(self.bot_token).build()

            # Setup handlers
            self.setup_handlers()

            # Initialize and start the application
            await self.application.initialize()
            await self.application.start()

            # Ensure webhook is disabled and drop pending updates, then start polling
            try:
                await self.application.bot.delete_webhook(drop_pending_updates=True)
            except Exception:
                pass

            logger.info("🤖 Bot starting polling...")
            self.running = True

            # Set slash command suggestions
            await self.set_bot_commands()

            # Start polling without taking over the event loop
            await self.application.updater.start_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )

            # Keep running until stop() toggles the flag
            while self.running:
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

    async def stop(self):
        """Stop the bot gracefully."""
        try:
            self.running = False
            if self.application:
                try:
                    await self.application.updater.stop()
                except Exception:
                    pass
                await self.application.stop()
                await self.application.shutdown()
                logger.info("🛑 Bot stopped gracefully")
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")

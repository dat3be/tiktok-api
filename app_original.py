from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
import os
import logging
from handlers.start import start
from handlers.user import get_user
from handlers.video import get_video

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Telegram Bot Token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    """
    Starts the bot and handles commands.
    """
    # Create the Application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("user", get_user))
    application.add_handler(CommandHandler("video", get_video))  # Add /video command

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()

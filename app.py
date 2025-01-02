from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
import logging
from colorlog import ColoredFormatter
from handlers.start import start
from handlers.user import get_user
from handlers.video import get_video, view_comments


# Set up colored logging
LOG_FORMAT = "%(log_color)s%(asctime)s - [%(levelname)s] - %(message)s"
formatter = ColoredFormatter(
    LOG_FORMAT,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Verify if TIKAPI_KEY is loaded
API_KEY = os.getenv("TIKAPI_KEY")
if not API_KEY:
    logger.error("TIKAPI_KEY is missing in environment variables. Check your .env file.")
else:
    logger.info("TIKAPI_KEY successfully loaded.")

# Verify if BOT_TOKEN is loaded
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is missing in environment variables. Check your .env file.")
else:
    logger.info("BOT_TOKEN successfully loaded.")


def main():
    """
    Starts the bot and handles commands.
    """
    try:
        # Create the Application instance
        application = Application.builder().token(BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("user", get_user))
        application.add_handler(CommandHandler("video", get_video))  # Add /video command

        # Add callback query handler for "View Comments"
        application.add_handler(CallbackQueryHandler(view_comments, pattern="^view_comments:"))

        logger.info("Bot is starting...")

        # Start the Bot
        application.run_polling()

    except Exception as e:
        logger.critical(f"Critical error occurred: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()

from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a welcome message when the user starts the bot.
    """
    await update.message.reply_text(
        "Welcome to the TikTok User Info Bot!\n"
        "Use /user <username> to fetch user information.\n"
        "Use /video <video_url> to fetch video information."
    )

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.tikapi_client import fetch_video_info

async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetch TikTok video information using /video command.
    """
    try:
        if not context.args:
            await update.message.reply_text(
                "Please provide a TikTok video URL. Example: /video <video_url>"
            )
            return

        video_url = context.args[0]
        video_info, keyboard = fetch_video_info(video_url)

        await update.message.reply_text(video_info, reply_markup=keyboard, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

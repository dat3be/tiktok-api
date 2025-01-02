from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.tikapi_client import fetch_video_info
from utils.tikapi_client import api, fetch_video_comments

async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetch TikTok video information using /video command.
    """
    try:
        # Check if the user has provided a TikTok video URL
        if not context.args:
            await update.message.reply_text(
                "❗ Please provide a TikTok video URL.\nExample: `/video <video_url>`",
                parse_mode="Markdown"
            )
            return

        video_url = context.args[0]

        # Fetch video information and keyboard from TikAPI
        video_info, keyboard = fetch_video_info(video_url)

        # Check if an error occurred during fetching
        if not keyboard:
            await update.message.reply_text(f"❗ {video_info}")
            return

        # Send the formatted video information along with the keyboard
        await update.message.reply_text(video_info, reply_markup=keyboard, parse_mode="Markdown")

    except Exception as e:
        # Handle unexpected errors
        await update.message.reply_text(f"❗ An error occurred: {str(e)}")

async def view_comments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetch and display comments for a given TikTok video.
    """
    try:
        # Acknowledge the button click immediately
        query = update.callback_query
        await query.answer("Fetching comments, please wait...")

        # Extract video ID from the callback query data
        video_id = query.data.split(":")[1]

        # Send a "loading" message to inform the user
        loading_message = await query.message.reply_text("⏳ Fetching comments, this may take a moment...")

        # Fetch comments using the TikAPI client
        comments = fetch_video_comments(video_id)

        # Update the message with the comments
        await loading_message.edit_text(comments, parse_mode="Markdown")

    except Exception as e:
        # Handle any errors and notify the user
        await query.message.reply_text(f"An error occurred: {str(e)}")
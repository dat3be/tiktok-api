from telegram import Update
from telegram.ext import ContextTypes
from utils.tikapi_client import fetch_user_info

async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetch TikTok user information using /user command.
    """
    try:
        if not context.args:
            await update.message.reply_text(
                "Please provide a username. Example: /user datngo2994"
            )
            return

        username = context.args[0]
        user_info = fetch_user_info(username)

        await update.message.reply_text(user_info, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

from tikapi import TikAPI, ValidationException, ResponseException
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

# Load TikAPI Key from environment variables
API_KEY = os.getenv("TIKAPI_KEY")
if not API_KEY:
    raise Exception("TIKAPI_KEY not found in environment variables")

# Debug: Log the loaded API key (remove this in production)
print(f"DEBUG: Loaded API Key: {API_KEY}")

# Initialize TikAPI client
api = TikAPI(API_KEY)


def fetch_user_info(username):
    """
    Fetch user information from TikAPI.
    Args:
        username (str): The username of the TikTok user.

    Returns:
        str: A formatted message containing user information or an error message.
    """
    try:
        response = api.public.check(username=username, country="us")
        user_data = response.json().get("userInfo", {})
        user_stats = user_data.get("stats", {})
        user_profile = user_data.get("user", {})

        # Extract relevant user data
        nickname = user_profile.get("nickname", "N/A")
        followers = user_stats.get("followerCount", "N/A")
        following = user_stats.get("followingCount", "N/A")
        likes = user_stats.get("heartCount", "N/A")
        video_count = user_stats.get("videoCount", "N/A")

        # Format the response message
        return (
            f"👤 **Username**: {username}\n"
            f"📛 **Nickname**: {nickname}\n"
            f"👥 **Followers**: {followers}\n"
            f"🔗 **Following**: {following}\n"
            f"❤️ **Likes**: {likes}\n"
            f"🎥 **Videos**: {video_count}\n"
        )

    except ValidationException as e:
        return f"Validation error: {e}, field: {e.field}"

    except ResponseException as e:
        return f"Response error: {e}, status code: {e.response.status_code}"

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def fetch_video_info(video_url):
    """
    Fetch video information from TikAPI.
    Args:
        video_url (str): The URL of the TikTok video.

    Returns:
        tuple: A formatted message and an InlineKeyboardMarkup for the video or an error message.
    """
    try:
        # Extract the video ID from the URL
        video_id = video_url.split("/")[-1]
        response = api.public.video(id=video_id)
        video_data = response.json().get("itemInfo", {}).get("itemStruct", {})

        # Extract video and author details
        author = video_data.get("author", {})
        stats = video_data.get("stats", {})

        username = author.get("uniqueId", "N/A")
        nickname = author.get("nickname", "N/A")
        video_desc = video_data.get("desc", "N/A")
        play_count = stats.get("playCount", "N/A")
        likes = stats.get("diggCount", "N/A")
        shares = stats.get("shareCount", "N/A")
        comments = stats.get("commentCount", "N/A")

        # Format the message
        message = (
            f"🎥 **Video Information**\n"
            f"👤 **Username**: {username}\n"
            f"📛 **Nickname**: {nickname}\n"
            f"📝 **Description**: {video_desc}\n"
            f"👁️ **Views**: {play_count}\n"
            f"❤️ **Likes**: {likes}\n"
            f"💬 **Comments**: {comments}\n"
            f"🔗 **Shares**: {shares}\n"
        )

        # Add a button to redirect users to the TikTok video downloader bot
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Download Video via @downloader_tiktok_bot", url="https://t.me/downloader_tiktok_bot")]
        ])

        return message, keyboard

    except ValidationException as e:
        return f"Validation error: {e}, field: {e.field}", None

    except ResponseException as e:
        return f"Response error: {e}, status code: {e.response.status_code}", None

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", None

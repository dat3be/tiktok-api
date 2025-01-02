from tikapi import TikAPI, ValidationException, ResponseException
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import re

# Load TikAPI Key from environment variables
API_KEY = os.getenv("TIKAPI_KEY")
if not API_KEY:
    raise Exception("TIKAPI_KEY not found in environment variables")

# Debug: Log the loaded API key (remove this in production)
print(f"DEBUG: Loaded API Key: {API_KEY}")

# Initialize TikAPI client
api = TikAPI(API_KEY)

def extract_username(url_or_username):
    """
    Extracts the TikTok username from a full URL or returns the provided username.
    Args:
        url_or_username (str): Either a full TikTok URL or a plain username.
    Returns:
        str: The extracted username.
    """
    # Regex to match TikTok profile URLs
    match = re.match(r"https?://www\.tiktok\.com/@([a-zA-Z0-9._-]+)", url_or_username)
    if match:
        return match.group(1)  # Return the extracted username
    return url_or_username  # Return as is if not a URL

def fetch_user_info(url_or_username):
    """
    Fetch user information from TikAPI.
    Args:
        url_or_username (str): The TikTok username or profile URL.
    Returns:
        str: A formatted message containing user information or an error message.
    """
    try:
        # Extract username from the input
        username = extract_username(url_or_username)

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

def extract_video_id(url_or_id):
    """
    Extracts the TikTok video ID from a full URL, short URL, or returns the ID as is.
    Args:
        url_or_id (str): Either a TikTok video URL or a plain video ID.
    Returns:
        str: The extracted video ID.
    """
    # Regex to match TikTok video URLs
    match = re.match(r"https?://(www\.)?tiktok\.com/.+/video/(\d+)", url_or_id)
    if match:
        return match.group(2)  # Return the extracted video ID

    # Regex to match short TikTok video links (e.g., vm.tiktok.com/abcdef)
    short_match = re.match(r"https?://vm\.tiktok\.com/([a-zA-Z0-9]+)/?", url_or_id)
    if short_match:
        return short_match.group(1)  # Return the extracted short ID

    return url_or_id  # Return as is if it's already a video ID

def fetch_video_info(url_or_id):
    """
    Fetch video information from TikAPI.
    Args:
        url_or_id (str): The TikTok video URL, short link, or video ID.
    Returns:
        tuple: A formatted message and an InlineKeyboardMarkup for the video or an error message.
    """
    try:
        # Extract the video ID from the URL or input
        video_id = extract_video_id(url_or_id)

        # Fetch video information
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

        # Add buttons for downloading video and viewing comments
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📥 Download Video via @downloader_tiktok_bot",
                    url="https://t.me/downloader_tiktok_bot"
                ),
                InlineKeyboardButton(
                    "💬 View Comments",
                    callback_data=f"view_comments:{video_id}"  # Use callback_data for the comments button
                )
            ]
        ])

        return message, keyboard

    except ValidationException as e:
        return f"Validation error: {e}, field: {e.field}", None

    except ResponseException as e:
        return f"Response error: {e}, status code: {e.response.status_code}", None

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", None

def fetch_video_comments(video_id):
    """
    Fetch comments for a given TikTok video.
    Args:
        video_id (str): The ID of the TikTok video.

    Returns:
        str: A formatted string of the top comments or an error message.
    """
    try:
        # Fetch the first batch of comments
        response = api.public.commentsList(media_id=video_id, count=10)

        # Parse the first batch of comments
        comments = response.json().get("comments", [])
        if not comments:
            return "No comments found for this video."

        # Format the first batch of comments
        formatted_comments = []
        for c in comments:
            text = c.get("text", "N/A")
            user = c.get("user", {})
            username = user.get("uniqueId", "N/A")
            profile_link = f"https://www.tiktok.com/@{username}" if username != "N/A" else "N/A"
            formatted_comments.append(
                f"💬 {text} - by [{username}]({profile_link})"
            )

        # Iterate through additional comments if available
        while response:
            cursor = response.json().get("cursor")
            response = response.next_items()
            if response:
                more_comments = response.json().get("comments", [])
                for c in more_comments:
                    text = c.get("text", "N/A")
                    user = c.get("user", {})
                    username = user.get("uniqueId", "N/A")
                    profile_link = f"https://www.tiktok.com/@{username}" if username != "N/A" else "N/A"
                    formatted_comments.append(
                        f"💬 {text} - by [{username}]({profile_link})"
                    )

        # Combine and return the formatted comments
        return "📃 **Top Comments**:\n" + "\n".join(formatted_comments[:10])  # Limit to 10 comments for display

    except ValidationException as e:
        return f"Validation error: {e}, field: {e.field}"

    except ResponseException as e:
        return f"Response error: {e}, status code: {e.response.status_code}"

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"




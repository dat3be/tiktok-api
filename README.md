
# TikTok API Bot

A Telegram bot powered by TikAPI to fetch TikTok user and video information. This bot allows users to retrieve detailed statistics about TikTok accounts and videos and provides a link to download videos via another Telegram bot.

---

## Features

- Fetch TikTok user information:
  - Followers
  - Following
  - Total likes
  - Total videos
  - Nickname
- Fetch TikTok video information:
  - Description
  - Views
  - Likes
  - Comments
  - Shares
  - Download link via a Telegram bot (@downloader_tiktok_bot).

---

## Project Structure

```
tiktok-api/
├── app.py                 # Main application entry point
├── handlers/              # Telegram bot command handlers
│   ├── __init__.py
│   ├── start.py           # /start command
│   ├── user.py            # /user command
│   ├── video.py           # /video command
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── tikapi_client.py   # TikAPI client integration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (excluded from Git)
└── README.md              # Project documentation
```

---

## Prerequisites

- Python 3.9 or higher
- A Telegram bot token ([Get it from BotFather](https://core.telegram.org/bots#botfather))
- A TikAPI account and API key ([Sign up here](https://tikapi.io))

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/tiktok-api.git
   cd tiktok-api
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   TIKAPI_KEY=your-tikapi-key
   BOT_TOKEN=your-telegram-bot-token
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

---

## Usage

### Commands

1. **Start the Bot**
   - Command: `/start`
   - Description: Displays a welcome message with instructions.

2. **Fetch User Info**
   - Command: `/user <username>`
   - Example: `/user datngo2994`

3. **Fetch Video Info**
   - Command: `/video <video_url>`
   - Example: `/video https://www.tiktok.com/@username/video/video_id`

   - Returns:
     - Author details
     - Video statistics
     - A download button linking to `@downloader_tiktok_bot`.

---

## Environment Variables

| Variable      | Description                    |
|---------------|--------------------------------|
| `TIKAPI_KEY`  | Your TikAPI key for accessing TikTok data. |
| `BOT_TOKEN`   | Your Telegram bot token.       |

---

## Dependencies

The project requires the following Python packages:

- `python-dotenv`
- `tikapi`
- `python-telegram-bot`

Install them using:
```bash
pip install -r requirements.txt
```

---

## Future Improvements

- Add more TikTok data endpoints (e.g., trending videos, hashtags).
- Improve error handling and logging.
- Add a frontend dashboard for managing requests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [TikAPI Documentation](https://tikapi.io/documentation/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

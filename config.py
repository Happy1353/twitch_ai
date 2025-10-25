"""
Configuration module for Twitch AI Girl
"""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# PATHS 
PROJECT_ROOT = Path(__file__).parent

# Twitch Settings
TWITCH_TOKEN = os.getenv('TWITCH_TOKEN', '')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID', '')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL', '')
TWITCH_BOT_NAME = os.getenv('TWITCH_BOT_NAME', '')

# AI Settings (supports Groq, DeepSeek, OpenAI, or any OpenAI-compatible API)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Can be Groq key (FREE!), DeepSeek key, or OpenAI key

# Character Settings
CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'Лиза')
CHARACTER_PERSONALITY = os.getenv(
    'CHARACTER_PERSONALITY',
    'Ты привлекательная и немного дерзкая стримерша. Отвечай кокетливо, с юмором и небольшой долей флирта. Будь дружелюбной и интересной.'
)

# Audio Settings
AUDIO_OUTPUT_DIR = 'output/audio'
# Note: Using gTTS (Google TTS) for voice generation - free alternative
# Voice customization is limited with gTTS, but it's free and works well

# Avatar Settings
AVATAR_IMAGE_PATH = 'assets/avatar_idle.png'
AVATAR_MOUTH_OPEN_PATH = 'assets/avatar_talking.png'
FRAME_RATE = 30
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Response Settings
MAX_RESPONSE_LENGTH = 200  # Maximum characters for response
MESSAGE_COOLDOWN = 5  # Seconds between responses

BANNED_WORDS_FILE = PROJECT_ROOT / 'res/banned_words.txt'
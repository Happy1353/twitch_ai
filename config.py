"""
Configuration module for Twitch AI Girl
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Twitch Settings
TWITCH_TOKEN = os.getenv('TWITCH_TOKEN', '')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID', '')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL', '')
TWITCH_BOT_NAME = os.getenv('TWITCH_BOT_NAME', '')

# OpenAI Settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Character Settings
CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'Лиза')
CHARACTER_PERSONALITY = os.getenv(
    'CHARACTER_PERSONALITY',
    'Ты привлекательная и немного дерзкая стримерша. Отвечай кокетливо, с юмором и небольшой долей флирта. Будь дружелюбной и интересной.'
)

# Audio Settings
AUDIO_OUTPUT_DIR = 'output/audio'
VOICE_MODEL = 'alloy'  # OpenAI TTS voices: alloy, echo, fable, onyx, nova, shimmer

# Avatar Settings
AVATAR_IMAGE_PATH = 'assets/avatar_idle.png'
AVATAR_MOUTH_OPEN_PATH = 'assets/avatar_talking.png'
FRAME_RATE = 30
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Response Settings
MAX_RESPONSE_LENGTH = 200  # Maximum characters for response
MESSAGE_COOLDOWN = 5  # Seconds between responses


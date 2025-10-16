"""
Utility script to test setup and configuration
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config


def test_configuration():
    """Test if configuration is properly set up"""
    print("=" * 60)
    print("🔍 ПРОВЕРКА КОНФИГУРАЦИИ")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # Check Twitch configuration
    print("\n📺 Twitch Configuration:")
    if config.TWITCH_TOKEN:
        print(f"  ✓ TWITCH_TOKEN: {'*' * 20}{config.TWITCH_TOKEN[-10:]}")
    else:
        errors.append("TWITCH_TOKEN не установлен")
        print("  ❌ TWITCH_TOKEN: не установлен")
    
    if config.TWITCH_CLIENT_ID:
        print(f"  ✓ TWITCH_CLIENT_ID: {config.TWITCH_CLIENT_ID[:10]}...")
    else:
        errors.append("TWITCH_CLIENT_ID не установлен")
        print("  ❌ TWITCH_CLIENT_ID: не установлен")
    
    if config.TWITCH_CHANNEL:
        print(f"  ✓ TWITCH_CHANNEL: {config.TWITCH_CHANNEL}")
    else:
        errors.append("TWITCH_CHANNEL не установлен")
        print("  ❌ TWITCH_CHANNEL: не установлен")
    
    if config.TWITCH_BOT_NAME:
        print(f"  ✓ TWITCH_BOT_NAME: {config.TWITCH_BOT_NAME}")
    else:
        warnings.append("TWITCH_BOT_NAME не установлен (будет использован токен бота)")
        print("  ⚠ TWITCH_BOT_NAME: не установлен")
    
    # Check OpenAI configuration
    print("\n🤖 OpenAI Configuration:")
    if config.OPENAI_API_KEY:
        print(f"  ✓ OPENAI_API_KEY: sk-...{config.OPENAI_API_KEY[-10:]}")
    else:
        errors.append("OPENAI_API_KEY не установлен")
        print("  ❌ OPENAI_API_KEY: не установлен")
    
    # Check character configuration
    print("\n👧 Character Configuration:")
    print(f"  ✓ CHARACTER_NAME: {config.CHARACTER_NAME}")
    print(f"  ✓ VOICE_MODEL: {config.VOICE_MODEL}")
    print(f"  ✓ PERSONALITY: {config.CHARACTER_PERSONALITY[:50]}...")
    
    # Check directories
    print("\n📁 Directories:")
    assets_dir = Path("assets")
    if assets_dir.exists():
        print(f"  ✓ assets/ существует")
    else:
        print(f"  ⚠ assets/ не существует (будет создана автоматически)")
    
    output_dir = Path(config.AUDIO_OUTPUT_DIR)
    if output_dir.exists():
        print(f"  ✓ {config.AUDIO_OUTPUT_DIR}/ существует")
    else:
        print(f"  ⚠ {config.AUDIO_OUTPUT_DIR}/ не существует (будет создана автоматически)")
    
    # Check avatar images
    print("\n🎨 Avatar Images:")
    idle_path = Path(config.AVATAR_IMAGE_PATH)
    if idle_path.exists():
        print(f"  ✓ {config.AVATAR_IMAGE_PATH} найден")
    else:
        print(f"  ⚠ {config.AVATAR_IMAGE_PATH} не найден (будет создан placeholder)")
    
    talking_path = Path(config.AVATAR_MOUTH_OPEN_PATH)
    if talking_path.exists():
        print(f"  ✓ {config.AVATAR_MOUTH_OPEN_PATH} найден")
    else:
        print(f"  ⚠ {config.AVATAR_MOUTH_OPEN_PATH} не найден (будет создан placeholder)")
    
    # Test imports
    print("\n📦 Dependencies:")
    try:
        import twitchio
        print(f"  ✓ twitchio v{twitchio.__version__}")
    except ImportError:
        errors.append("twitchio не установлен")
        print("  ❌ twitchio не установлен")
    
    try:
        import openai
        print(f"  ✓ openai v{openai.__version__}")
    except ImportError:
        errors.append("openai не установлен")
        print("  ❌ openai не установлен")
    
    try:
        import pygame
        print(f"  ✓ pygame v{pygame.version.ver}")
    except ImportError:
        errors.append("pygame не установлен")
        print("  ❌ pygame не установлен")
    
    try:
        import cv2
        print(f"  ✓ opencv-python v{cv2.__version__}")
    except ImportError:
        errors.append("opencv-python не установлен")
        print("  ❌ opencv-python не установлен")
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("❌ НАЙДЕНЫ ОШИБКИ:")
        for error in errors:
            print(f"  • {error}")
        print("\n⚠ Пожалуйста, исправьте ошибки перед запуском")
        print("📖 См. setup_guide.md для подробных инструкций")
        return False
    elif warnings:
        print("⚠ НАЙДЕНЫ ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"  • {warning}")
        print("\n✓ Можно запускать, но рекомендуется исправить предупреждения")
        return True
    else:
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("\n🚀 Готово к запуску: python main.py")
        return True


if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)


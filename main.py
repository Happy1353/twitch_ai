"""
Main application - Twitch AI Girl Streamer (VRM Edition)
"""
import asyncio
import time
import threading
from datetime import datetime
import config
from utils.mok_chat import start_mok_bot
from twitch_chat import start_chat_bot
from ai_brain import AIBrain
from voice_engine import VoiceEngine
from avatar_animator import AvatarAnimator
from web_server import start_server
import sys
from utils.message_filter import MessageFilter
from data.db import AppDb

class TwitchAIGirl:
    """Main application class"""
    
    def __init__(self, mode):
        """Initialize application"""
        print("=" * 60)
        print(f"🎀 Twitch AI Girl - {config.CHARACTER_NAME}")
        print("=" * 60)
        # Mode 
        self.mode = mode

        # Initialize components
        self.ai_brain = AIBrain()
        self.voice_engine = VoiceEngine()
        self.avatar = AvatarAnimator()
        self.chat_bot = None
        
        # State
        self.last_response_time = 0
        self.is_processing = False
        self.message_queue = asyncio.Queue()
        
        # Filter 
        self.message_filter = MessageFilter()

    async def process_message(self, username: str, message: str):
        """
        Process incoming chat message
        
        Args:
            username: Username who sent the message
            message: Message content
        """
        # Check cooldown
        current_time = time.time()
        if self.mode != 'no_bot' and current_time - self.last_response_time < config.MESSAGE_COOLDOWN:
            print(f"⏳ Cooldown active, skipping message from {username}")
            return
        
        # Check if already processing
        if self.is_processing:
            print(f"⏳ Уже обрабатываю сообщение, пропускаю: {username}")
            return
        
        if self.message_filter.should_ignore_message(username, message):
            print(f"Плохое сообщение，пропускаю: {username}")
            return

        self.is_processing = True
        
        try:
            # Get AI response
            print(f"\n🤖 Генерация ответа для {username}...")
            response = await self.ai_brain.get_response(username, message)
            
            if not response:
                return
            
            print(f"💭 Ответ: {response}")
            
            # Generate audio file
            audio_file = await self.voice_engine.text_to_speech(response)
            
            if not audio_file:
                print("❌ Не удалось сгенерировать аудио")
                return
            
            # Get audio duration
            duration = await self.voice_engine.get_audio_duration(audio_file)
            
            # Start talking animation
            await self.avatar.start_talking()
            
            # Send audio to browser for playback
            await self.avatar.vrm_controller.play_audio(audio_file)
            
            # Wait for audio to finish
            await asyncio.sleep(duration)
            
            # Stop talking animation
            await self.avatar.stop_talking()
            
            # Clean up audio file
            import os
            try:
                os.remove(audio_file)
            except:
                pass
            
            print(f"✓ Ответ воспроизведен ({duration:.1f}s)\n")
            
            self.last_response_time = time.time()
            
        except Exception as e:
            print(f"❌ Ошибка обработки сообщения: {e}")
            await self.avatar.stop_talking()
        finally:
            self.is_processing = False
    
    async def start(self):
        """Start the application"""
        print("\n🚀 Запуск приложения...\n")
        
        # Validate configuration
        if not self._validate_config():
            return
        
        # Start HTTP server for VRM viewer (in separate thread)
        print("🌐 Запуск HTTP сервера...")
        http_thread = threading.Thread(target=start_server, daemon=True)
        http_thread.start()
        
        # Give HTTP server time to start
        await asyncio.sleep(1)
        
        # Start avatar (WebSocket server + browser)
        print("🎨 Запуск VRM аватара...")
        avatar_task = asyncio.create_task(self.avatar.start())
        
        # Give browser time to open
        await asyncio.sleep(3)
        # Start chat bot
        if self.mode == 'no_bot':
            print("Подключение к файлу...")
            self.chat_bot = await start_mok_bot(self.process_message)
        else:
            print("💬 Подключение к Twitch чату...")
            self.chat_bot = await start_chat_bot(self.process_message)
        
        print("\n" + "=" * 60)
        print("✨ ВСЕ СИСТЕМЫ ЗАПУЩЕНЫ! ✨")
        print("=" * 60)
        print(f"Канал: {config.TWITCH_CHANNEL}")
        print(f"Персонаж: {config.CHARACTER_NAME}")
        print("=" * 60)
        print("\nОжидание сообщений в чате...")
        print("Закройте браузер или нажмите Ctrl+C для выхода\n")
        
        # Run bot
        try:
            await self.chat_bot.start()
        except KeyboardInterrupt:
            print("\n\n👋 Завершение работы...")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
        finally:
            await self.cleanup()
    
    def _validate_config(self) -> bool:
        """Validate configuration"""
        errors = []
        
        if not config.TWITCH_TOKEN:
            errors.append("TWITCH_TOKEN не установлен")
        if not config.TWITCH_CHANNEL:
            errors.append("TWITCH_CHANNEL не установлен")
        if not config.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY не установлен (Groq ключ)")
        
        if errors:
            print("❌ ОШИБКИ КОНФИГУРАЦИИ:")
            for error in errors:
                print(f"  - {error}")
            print("\n⚠ Пожалуйста, настройте файл .env")
            print("Скопируйте .env.example в .env и заполните необходимые параметры")
            print("📖 См. SETUP_GROQ.md для инструкций")
            return False
        
        return True
    
    async def cleanup(self):
        """Cleanup resources"""
        print("🧹 Очистка ресурсов...")
        
        if self.voice_engine:
            self.voice_engine.stop()
        
        if self.avatar:
            await self.avatar.stop()
        
        print("✓ Завершено")


async def main(mode):
    """Main entry point"""
    app = TwitchAIGirl(mode)
    await app.start()


if __name__ == "__main__":
    try:
        mode = sys.argv[2] if len(sys.argv) > 2 else 'full'
        asyncio.run(main(mode))
    except KeyboardInterrupt:
        print("\n👋 До свидания!")

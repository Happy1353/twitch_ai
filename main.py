"""
Main application - Twitch AI Girl Streamer (macOS compatible with pygame)
"""
import asyncio
import time
import threading
import pygame
from datetime import datetime
import config
from twitch_chat import start_chat_bot
from ai_brain import AIBrain
from voice_engine import VoiceEngine
from avatar_animator import AvatarAnimator


class TwitchAIGirl:
    """Main application class"""
    
    def __init__(self):
        """Initialize application"""
        print("=" * 60)
        print(f"🎀 Twitch AI Girl - {config.CHARACTER_NAME}")
        print("=" * 60)
        
        # Initialize components
        self.ai_brain = AIBrain()
        self.voice_engine = VoiceEngine()
        self.avatar = AvatarAnimator()
        self.chat_bot = None
        
        # State
        self.last_response_time = 0
        self.is_processing = False
        self.message_queue = asyncio.Queue()
        
        # Pygame
        self.screen = None
        self.clock = None
        
    async def process_message(self, username: str, message: str):
        """
        Process incoming chat message
        
        Args:
            username: Username who sent the message
            message: Message content
        """
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_response_time < config.MESSAGE_COOLDOWN:
            print(f"⏳ Cooldown active, skipping message from {username}")
            return
        
        # Check if already processing
        if self.is_processing:
            print(f"⏳ Уже обрабатываю сообщение, пропускаю: {username}")
            return
        
        self.is_processing = True
        
        try:
            # Get AI response
            print(f"\n🤖 Генерация ответа для {username}...")
            response = await self.ai_brain.get_response(username, message)
            
            if not response:
                return
            
            print(f"💭 Ответ: {response}")
            
            # Convert to speech and play
            duration = await self.voice_engine.speak(
                response,
                on_start=self.avatar.start_talking,
                on_end=self.avatar.stop_talking
            )
            
            print(f"✓ Ответ воспроизведен ({duration:.1f}s)\n")
            
            self.last_response_time = time.time()
            
        except Exception as e:
            print(f"❌ Ошибка обработки сообщения: {e}")
        finally:
            self.is_processing = False
    
    async def start_bot_async(self):
        """Start Twitch bot in async thread"""
        try:
            print("💬 Подключение к Twitch чату...")
            self.chat_bot = await start_chat_bot(self.process_message)
            
            print("\n" + "=" * 60)
            print("✨ ВСЕ СИСТЕМЫ ЗАПУЩЕНЫ! ✨")
            print("=" * 60)
            print(f"Канал: {config.TWITCH_CHANNEL}")
            print(f"Персонаж: {config.CHARACTER_NAME}")
            print("=" * 60)
            print("\nОжидание сообщений в чате...")
            print("Нажмите ESC в окне аватара для выхода\n")
            
            await self.chat_bot.start()
        except Exception as e:
            print(f"❌ Ошибка бота: {e}")
            self.avatar.running = False
    
    def start(self):
        """Start the application (synchronous main loop with pygame)"""
        print("\n🚀 Запуск приложения...\n")
        
        # Validate configuration
        if not self._validate_config():
            return
        
        # Initialize pygame display
        print("🎨 Инициализация окна...")
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(f"{config.CHARACTER_NAME} - Twitch Stream")
        self.clock = pygame.time.Clock()
        
        # Start avatar
        self.avatar.start()
        
        # Start Twitch bot in separate thread
        def run_bot():
            asyncio.run(self.start_bot_async())
        
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        # Give bot time to connect
        time.sleep(2)
        
        # Main pygame loop (must run in main thread on macOS)
        print("🎮 Запуск главного цикла...\n")
        try:
            while self.avatar.running:
                if not self.avatar.update(self.screen, self.clock):
                    break
        except KeyboardInterrupt:
            print("\n\n👋 Завершение работы...")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
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
    
    def cleanup(self):
        """Cleanup resources"""
        print("🧹 Очистка ресурсов...")
        
        if self.voice_engine:
            self.voice_engine.stop()
        
        if self.avatar:
            self.avatar.stop()
        
        pygame.quit()
        
        print("✓ Завершено")


def main():
    """Main entry point"""
    app = TwitchAIGirl()
    app.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 До свидания!")

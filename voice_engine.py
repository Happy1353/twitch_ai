"""
Voice Engine - Text-to-Speech module
"""
import asyncio
import os
from pathlib import Path
from gtts import gTTS
import pygame
import config
from typing import Callable, Optional


class VoiceEngine:
    """Handles text-to-speech conversion and playback"""
    
    def __init__(self):
        """Initialize voice engine"""
        # Using gTTS (Google Text-to-Speech) - Free alternative
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Create output directory
        Path(config.AUDIO_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        
        self.is_speaking = False
        self.current_audio_file: Optional[str] = None
        
    async def text_to_speech(self, text: str, callback: Optional[Callable] = None) -> str:
        """
        Convert text to speech and save to file
        
        Args:
            text: Text to convert
            callback: Optional callback function to call when speech starts/ends
            
        Returns:
            Path to generated audio file
        """
        try:
            # Generate unique filename
            import time
            filename = f"{config.AUDIO_OUTPUT_DIR}/speech_{int(time.time())}.mp3"
            
            print(f"🎤 Генерация речи: {text[:50]}...")
            
            # Generate speech using Google TTS (free alternative)
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: gTTS(text=text, lang='ru', slow=False).save(filename)
            )
            
            print(f"✓ Аудио сохранено: {filename}")
            
            self.current_audio_file = filename
            return filename
            
        except Exception as e:
            print(f"❌ Ошибка генерации речи: {e}")
            return ""
    
    async def play_audio(self, audio_file: str, on_start: Optional[Callable] = None, 
                        on_end: Optional[Callable] = None) -> float:
        """
        Play audio file
        
        Args:
            audio_file: Path to audio file
            on_start: Callback when audio starts
            on_end: Callback when audio ends
            
        Returns:
            Duration of audio in seconds
        """
        try:
            if not os.path.exists(audio_file):
                print(f"❌ Аудио файл не найден: {audio_file}")
                return 0
            
            self.is_speaking = True
            
            # Load and play audio
            pygame.mixer.music.load(audio_file)
            
            if on_start:
                on_start()
            
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            self.is_speaking = False
            
            if on_end:
                on_end()
            
            # Get audio duration (approximate)
            sound = pygame.mixer.Sound(audio_file)
            duration = sound.get_length()
            
            # Clean up old audio file
            try:
                os.remove(audio_file)
            except:
                pass
            
            return duration
            
        except Exception as e:
            print(f"❌ Ошибка воспроизведения: {e}")
            self.is_speaking = False
            return 0
    
    async def speak(self, text: str, on_start: Optional[Callable] = None, 
                   on_end: Optional[Callable] = None) -> float:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            on_start: Callback when speaking starts
            on_end: Callback when speaking ends
            
        Returns:
            Duration of speech in seconds
        """
        audio_file = await self.text_to_speech(text)
        if audio_file:
            return await self.play_audio(audio_file, on_start, on_end)
        return 0
    
    def stop(self):
        """Stop current playback"""
        pygame.mixer.music.stop()
        self.is_speaking = False


"""
Voice Engine - Text-to-Speech module with audio enhancement
"""
import asyncio
import os
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import config
from typing import Optional


class VoiceEngine:
    """Handles text-to-speech conversion and playback"""
    
    def __init__(self):
        """Initialize voice engine"""
        # Using gTTS (Google Text-to-Speech) - Free alternative
        # Audio will be played in browser, not locally
        
        # Create output directory
        Path(config.AUDIO_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        
        self.is_speaking = False
        self.current_audio_file: Optional[str] = None
        
    async def text_to_speech(self, text: str) -> str:
        """
        Convert text to speech and save to file
        
        Args:
            text: Text to convert
            
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
            
            print(f"✓ Аудио сгенерировано: {filename}")
            
            # Post-process audio to make it sound better
            enhanced_filename = await self._enhance_audio(filename)
            
            self.current_audio_file = enhanced_filename
            return enhanced_filename
            
        except Exception as e:
            print(f"❌ Ошибка генерации речи: {e}")
            return ""
    
    async def _enhance_audio(self, audio_file: str) -> str:
        """
        Enhance audio quality with post-processing
        
        Args:
            audio_file: Path to original audio file
            
        Returns:
            Path to enhanced audio file
        """
        try:
            print("🎵 Улучшение качества голоса...")
            
            # Load audio
            audio = AudioSegment.from_mp3(audio_file)
            
            # 1. Pitch shift to make voice higher/more feminine (+3 semitones)
            # Note: This is a simple speed-then-resample method
            octaves = 0.25  # ~3 semitones higher
            new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
            pitched_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
            pitched_audio = pitched_audio.set_frame_rate(audio.frame_rate)
            
            # 2. Normalize volume (make louder)
            normalized_audio = normalize(pitched_audio, headroom=0.1)
            
            # 3. Dynamic range compression (smoother, more professional)
            compressed_audio = compress_dynamic_range(
                normalized_audio,
                threshold=-20.0,
                ratio=4.0,
                attack=5.0,
                release=50.0
            )
            
            # 4. Add slight bass boost (warmth)
            # Low shelf filter at 200Hz
            bass_boosted = compressed_audio.low_pass_filter(8000).high_pass_filter(100)
            
            # Save enhanced audio
            enhanced_file = audio_file.replace('.mp3', '_enhanced.mp3')
            bass_boosted.export(enhanced_file, format='mp3', bitrate='128k')
            
            # Remove original file
            try:
                os.remove(audio_file)
            except:
                pass
            
            print("✓ Голос улучшен: +pitch, +громкость, +компрессия")
            
            return enhanced_file
            
        except Exception as e:
            print(f"⚠ Ошибка улучшения аудио: {e}, используем оригинал")
            return audio_file
    
    async def get_audio_duration(self, audio_file: str) -> float:
        """
        Get audio file duration
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            from mutagen.mp3 import MP3
            audio = MP3(audio_file)
            return audio.info.length
        except:
            # Fallback: estimate ~150 words per minute
            import os
            file_size = os.path.getsize(audio_file)
            # Rough estimate: 1 second per 4KB for speech
            return file_size / 4000
    
    def stop(self):
        """Stop current playback (cleanup)"""
        self.is_speaking = False


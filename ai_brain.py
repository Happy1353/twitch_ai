"""
AI Brain module - handles ChatGPT integration
"""
import asyncio
from openai import AsyncOpenAI
import config
from typing import List, Dict


class AIBrain:
    """Handles AI responses using OpenAI ChatGPT"""
    
    def __init__(self):
        """Initialize AI brain"""
        # Use Groq API (OpenAI-compatible, FREE!)
        self.client = AsyncOpenAI(
            api_key=config.OPENAI_API_KEY,  # Will use Groq key
            base_url="https://api.groq.com/openai/v1"
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10  # Keep last 10 messages for context
        
        # Initialize with character personality
        self.system_prompt = f"""Ты {config.CHARACTER_NAME} - виртуальная стримерша на Twitch.
{config.CHARACTER_PERSONALITY}

ВАЖНЫЕ ПРАВИЛА:
1. Отвечай КРАТКО (максимум 2-3 предложения)
2. Используй эмодзи умеренно 
3. Будь естественной и живой
4. Отвечай на русском языке
5. Можешь быть игривой и кокетливой
6. Иногда используй сленг и современные выражения
7. Помни, что ты общаешься со зрителями в чате
"""
        
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
        
    async def get_response(self, username: str, message: str) -> str:
        """
        Get AI response for a message
        
        Args:
            username: Username who sent the message
            message: Message content
            
        Returns:
            AI generated response
        """
        try:
            # Add user message to history
            user_message = f"{username} спрашивает: {message}"
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Get response from Groq (FREE!)
            response = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # NEW Groq model (updated Oct 2024)
                messages=self.conversation_history[-self.max_history:],  # Use recent history
                max_tokens=150,
                temperature=0.9,  # More creative responses
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Limit response length
            if len(ai_response) > config.MAX_RESPONSE_LENGTH:
                ai_response = ai_response[:config.MAX_RESPONSE_LENGTH] + "..."
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            # Trim history if too long
            if len(self.conversation_history) > self.max_history + 1:  # +1 for system prompt
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-(self.max_history):]
            
            return ai_response
            
        except Exception as e:
            print(f"❌ Ошибка AI: {e}")
            return "Ой, что-то пошло не так... 😅"
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = [self.conversation_history[0]]  # Keep system prompt


"""
Twitch chat integration module
"""
import asyncio
from twitchio.ext import commands
from typing import Callable, Optional
import config


class TwitchChatBot(commands.Bot):
    """Bot for reading Twitch chat messages"""
    
    def __init__(self, message_callback: Callable[[str, str], None]):
        """
        Initialize Twitch bot
        
        Args:
            message_callback: Function to call when new message arrives (username, message)
        """
        super().__init__(
            token=config.TWITCH_TOKEN,
            prefix='!',
            initial_channels=[config.TWITCH_CHANNEL]
        )
        self.message_callback = message_callback
        self.last_message_time = 0
        
    async def event_ready(self):
        """Called when bot is ready"""
        print(f'✓ Подключено к чату Twitch | Канал: {config.TWITCH_CHANNEL}')
        print(f'✓ Бот: {self.nick}')
        
    async def event_message(self, message):
        """Called when a message is received"""
        # Ignore messages from the bot itself
        if message.echo:
            return
            
        # Ignore commands
        if message.content.startswith('!'):
            await self.handle_commands(message)
            return
            
        # Process message
        username = message.author.name
        content = message.content
        
        print(f'💬 {username}: {content}')
        
        # Call the callback function
        if self.message_callback:
            await self.message_callback(username, content)
    
    @commands.command(name='привет')
    async def hello(self, ctx):
        """Test command"""
        await ctx.send(f'Привет, {ctx.author.name}! 💕')


async def start_chat_bot(message_callback: Callable[[str, str], None]) -> TwitchChatBot:
    """
    Start Twitch chat bot
    
    Args:
        message_callback: Function to call when new message arrives
        
    Returns:
        TwitchChatBot instance
    """
    bot = TwitchChatBot(message_callback)
    return bot


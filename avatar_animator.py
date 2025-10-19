"""
Avatar Animator - Controls VRM model via WebSocket
"""
import asyncio
import webbrowser
import time
from pathlib import Path
from typing import Optional
import config
from vrm_controller import VRMController


class AvatarAnimator:
    """Animates VRM avatar via WebSocket"""
    
    def __init__(self):
        """Initialize avatar animator"""
        self.window_name = f"{config.CHARACTER_NAME} - Twitch Stream"
        
        # Animation state
        self.is_talking = False
        self.running = False
        
        # VRM controller
        self.vrm_controller: Optional[VRMController] = None
        
        # Check if VRM file exists
        self.vrm_path = Path("assets/ai_girl.vrm")
        if not self.vrm_path.exists():
            print("⚠ VRM файл не найден: assets/ai_girl.vrm")
        else:
            print(f"✓ VRM модель найдена: {self.vrm_path}")
    
    async def start(self):
        """Start avatar display and WebSocket server"""
        self.running = True
        
        # Start WebSocket server
        self.vrm_controller = VRMController(port=8765)
        await self.vrm_controller.start()
        
        # Open browser with VRM viewer (using HTTP server)
        viewer_url = "http://localhost:3000/web/vrm_viewer.html"
        
        print(f"🌐 Открытие VRM viewer: {viewer_url}")
        print(f"⚠️ Если браузер не открылся, откройте вручную: {viewer_url}")
        
        webbrowser.open(viewer_url)
        
        print(f"✓ Аватар запущен: {self.window_name}")
        
        # Keep server running
        while self.running:
            await asyncio.sleep(0.1)
    
    async def stop(self):
        """Stop avatar display"""
        self.running = False
        if self.vrm_controller:
            await self.vrm_controller.stop()
    
    async def start_talking(self):
        """Start talking animation"""
        self.is_talking = True
        if self.vrm_controller:
            await self.vrm_controller.start_talking()
        print("👄 Начало речи")
    
    async def stop_talking(self):
        """Stop talking animation"""
        self.is_talking = False
        if self.vrm_controller:
            await self.vrm_controller.stop_talking()
        print("🤐 Конец речи")

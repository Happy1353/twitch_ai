"""
VRM Controller - WebSocket server for controlling VRM model animations
"""
import asyncio
import websockets
import json
import base64
from typing import Set, Optional


class VRMController:
    """Controls VRM model via WebSocket"""
    
    def __init__(self, port: int = 8765):
        """Initialize VRM controller"""
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server: Optional[websockets.WebSocketServer] = None
        self.is_running = False
        
    async def start(self):
        """Start WebSocket server"""
        self.is_running = True
        print(f"🌐 WebSocket сервер запущен на порту {self.port}")
        
        self.server = await websockets.serve(
            self._handle_client,
            "localhost",
            self.port
        )
        
    async def stop(self):
        """Stop WebSocket server"""
        self.is_running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
    async def _handle_client(self, websocket):
        """Handle new WebSocket client"""
        self.clients.add(websocket)
        print(f"✓ Клиент подключен: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                # Echo messages back (для отладки)
                pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"✗ Клиент отключен: {websocket.remote_address}")
    
    async def start_talking(self):
        """Send start talking command to all clients"""
        await self._broadcast({
            "action": "start_talking"
        })
        
    async def stop_talking(self):
        """Send stop talking command to all clients"""
        await self._broadcast({
            "action": "stop_talking"
        })
    
    async def play_audio(self, audio_file_path: str):
        """
        Send audio file to browser for playback
        
        Args:
            audio_file_path: Path to audio file
        """
        try:
            # Read audio file and encode to base64
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            await self._broadcast({
                "action": "play_audio",
                "audio": audio_base64
            })
            
            print(f"✓ Аудио отправлено в браузер ({len(audio_data)} bytes)")
            
        except Exception as e:
            print(f"❌ Ошибка отправки аудио: {e}")
    
    async def _broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return
            
        message_json = json.dumps(message)
        
        # Send to all clients
        websockets.broadcast(self.clients, message_json)


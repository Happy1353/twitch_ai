"""
Simple HTTP server for serving VRM viewer
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def start_server():
    """Start HTTP server"""
    # Change to project root
    os.chdir(Path(__file__).parent)
    
    handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🌐 HTTP сервер запущен на http://localhost:{PORT}")
        print(f"📂 Раздаю файлы из: {os.getcwd()}")
        print(f"🎨 Откройте VRM viewer: http://localhost:{PORT}/web/vrm_viewer.html")
        print("\nНажмите Ctrl+C для остановки")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Сервер остановлен")

if __name__ == "__main__":
    start_server()


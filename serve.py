"""
Simple HTTP server for viewing AgentFlow artifacts without full installation.
This serves the sandbox directory with CORS enabled for local development.
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 5050
DIRECTORY = Path(__file__).parent / "sandbox"

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS headers."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests and serve index.html for root."""
        if self.path == '/':
            self.path = '/viewer-standalone.html'
        return super().do_GET()

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("127.0.0.1", PORT), CORSRequestHandler) as httpd:
        print(f"╔═══════════════════════════════════════════════════════════╗")
        print(f"║  🚀 AgentFlow Gemini Adapter - Live Server               ║")
        print(f"╚═══════════════════════════════════════════════════════════╝")
        print(f"")
        print(f"  📂 Serving: {DIRECTORY}")
        print(f"  🌐 URL:     http://127.0.0.1:{PORT}")
        print(f"")
        print(f"  ✨ Open http://127.0.0.1:{PORT} in your browser")
        print(f"  ⛔ Press Ctrl+C to stop the server")
        print(f"")
        print(f"─" * 61)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n")
            print(f"🛑 Server stopped.")

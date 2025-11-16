"""
Simple HTTP Server để serve test.html
Chạy: python serve_test.py
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    
    print("="*60)
    print("TEST HTML SERVER")
    print("="*60)
    print(f"Server chạy tại: http://localhost:{port}")
    print(f"Mở test page: http://localhost:{port}/test.html")
    print("="*60)
    print("\nĐảm bảo API server đang chạy:")
    print("  python run.py")
    print("\nNhấn Ctrl+C để dừng server")
    print("="*60)
    
    # Auto open browser
    webbrowser.open(f'http://localhost:{port}/test.html')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer đã dừng!")

if __name__ == '__main__':
    run()
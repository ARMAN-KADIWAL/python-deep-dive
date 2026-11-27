#!/usr/bin/env python3
"""
Basic HTTP Server Example
This server demonstrates the foundation of handling HTTP requests
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        response = """
        <html>
        <body>
        <h1>Welcome to Our Simple HTTP Server!</h1>
        <p>This server is running and ready to handle requests.</p>
        <p>Current path: {}</p>
        </body>
        </html>
        """.format(self.path)
        
        self.wfile.write(response.encode('utf-8'))

def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()

#!/usr/bin/env python3
"""
Multi-Method HTTP Server
Handles GET, POST, PUT, and DELETE requests
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class MultiMethodHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "method": "GET",
            "path": self.path,
            "message": "GET request received successfully"
        }
        
        self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            # Try to parse JSON data
            json_data = json.loads(post_data.decode('utf-8'))
            
            self.send_response(201)  # Created
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {
                "method": "POST",
                "path": self.path,
                "message": "POST request received successfully",
                "received_data": json_data
            }
            
        except json.JSONDecodeError:
            self.send_response(400)  # Bad Request
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {
                "method": "POST",
                "path": self.path,
                "error": "Invalid JSON data"
            }
        
        self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
    
    def do_PUT(self):
        """Handle PUT requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        put_data = self.rfile.read(content_length)
        
        try:
            json_data = json.loads(put_data.decode('utf-8'))
            
            self.send_response(200)  # OK
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {
                "method": "PUT",
                "path": self.path,
                "message": "PUT request received successfully",
                "received_data": json_data
            }
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {
                "method": "PUT",
                "path": self.path,
                "error": "Invalid JSON data"
            }
        
        self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "method": "DELETE",
            "path": self.path,
            "message": "DELETE request received successfully"
        }
        
        self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))

def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, MultiMethodHandler)
    print(f"Multi-Method Server running on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()

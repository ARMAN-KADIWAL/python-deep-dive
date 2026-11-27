#!/usr/bin/env python3
"""
RESTful API Server with CRUD Operations
Manages a collection of users in memory
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import re

class RESTfulAPIHandler(BaseHTTPRequestHandler):
    # In-memory data storage (in a real application, this would be a database)
    users = {}
    next_id = 1
    
    def send_json_response(self, status_code, data):
        """Helper method to send JSON responses"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def parse_path(self):
        """Parse the URL path to extract resource and ID"""
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 1 and path_parts[0] == 'users':
            return 'users', None
        elif len(path_parts) == 2 and path_parts[0] == 'users':
            try:
                user_id = int(path_parts[1])
                return 'users', user_id
            except ValueError:
                return None, None
        return None, None
    
    def do_GET(self):
        """Handle GET requests - Read operations"""
        resource, user_id = self.parse_path()
        
        if resource == 'users':
            if user_id is None:
                # GET /users - Return all users
                self.send_json_response(200, {
                    "users": list(self.users.values()),
                    "total": len(self.users)
                })
            else:
                # GET /users/{id} - Return specific user
                if user_id in self.users:
                    self.send_json_response(200, self.users[user_id])
                else:
                    self.send_json_response(404, {
                        "error": f"User with ID {user_id} not found"
                    })
        else:
            self.send_json_response(404, {
                "error": "Resource not found",
                "available_endpoints": ["/users", "/users/{id}"]
            })
    
    def do_POST(self):
        """Handle POST requests - Create operations"""
        resource, user_id = self.parse_path()
        
        if resource == 'users' and user_id is None:
            # POST /users - Create new user
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                user_data = json.loads(post_data.decode('utf-8'))
                
                # Validate required fields
                required_fields = ['name', 'email']
                for field in required_fields:
                    if field not in user_data:
                        self.send_json_response(400, {
                            "error": f"Missing required field: {field}"
                        })
                        return
                
                # Create new user
                new_user = {
                    "id": self.next_id,
                    "name": user_data['name'],
                    "email": user_data['email'],
                    "age": user_data.get('age', None)
                }
                
                self.users[self.next_id] = new_user
                type(self).next_id += 1
                
                self.send_json_response(201, {
                    "message": "User created successfully",
                    "user": new_user
                })
                
            except json.JSONDecodeError:
                self.send_json_response(400, {
                    "error": "Invalid JSON data"
                })
        else:
            self.send_json_response(405, {
                "error": "Method not allowed for this endpoint"
            })
    
    def do_PUT(self):
        """Handle PUT requests - Update operations"""
        resource, user_id = self.parse_path()
        
        if resource == 'users' and user_id is not None:
            # PUT /users/{id} - Update existing user
            if user_id not in self.users:
                self.send_json_response(404, {
                    "error": f"User with ID {user_id} not found"
                })
                return
            
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                put_data = self.rfile.read(content_length)
                update_data = json.loads(put_data.decode('utf-8'))
                
                # Update user data
                user = self.users[user_id]
                if 'name' in update_data:
                    user['name'] = update_data['name']
                if 'email' in update_data:
                    user['email'] = update_data['email']
                if 'age' in update_data:
                    user['age'] = update_data['age']
                
                self.send_json_response(200, {
                    "message": "User updated successfully",
                    "user": user
                })
                
            except json.JSONDecodeError:
                self.send_json_response(400, {
                    "error": "Invalid JSON data"
                })
        else:
            self.send_json_response(405, {
                "error": "Method not allowed or invalid endpoint"
            })
    
    def do_DELETE(self):
        """Handle DELETE requests - Delete operations"""
        resource, user_id = self.parse_path()
        
        if resource == 'users' and user_id is not None:
            # DELETE /users/{id} - Delete specific user
            if user_id in self.users:
                deleted_user = self.users.pop(user_id)
                self.send_json_response(200, {
                    "message": "User deleted successfully",
                    "deleted_user": deleted_user
                })
            else:
                self.send_json_response(404, {
                    "error": f"User with ID {user_id} not found"
                })
        else:
            self.send_json_response(405, {
                "error": "Method not allowed or invalid endpoint"
            })
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8000):
    """Start the RESTful API server"""
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, RESTfulAPIHandler)
    print(f"RESTful API Server running on http://localhost:{port}")
    print("Available endpoints:")
    print("  GET    /users      - Get all users")
    print("  GET    /users/{id} - Get specific user")
    print("  POST   /users      - Create new user")
    print("  PUT    /users/{id} - Update existing user")
    print("  DELETE /users/{id} - Delete user")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()

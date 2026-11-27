#!/usr/bin/env python3
"""
Advanced RESTful API with Enhanced JSON Parsing and Validation
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import re
from datetime import datetime

class AdvancedAPIHandler(BaseHTTPRequestHandler):
    # Enhanced in-memory storage with metadata
    users = {}
    next_id = 1
    
    def send_json_response(self, status_code, data):
        """Enhanced JSON response with timestamp"""
        response_data = {
            "timestamp": datetime.now().isoformat(),
            "status": status_code,
            **data
        }
        
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_user_data(self, data, is_update=False):
        """Comprehensive user data validation"""
        errors = []
        
        # Check for required fields (only for creation)
        if not is_update:
            required_fields = ['name', 'email']
            for field in required_fields:
                if field not in data or not data[field]:
                    errors.append(f"Missing or empty required field: {field}")
        
        # Validate name
        if 'name' in data:
            if not isinstance(data['name'], str) or len(data['name'].strip()) < 2:
                errors.append("Name must be a string with at least 2 characters")
        
        # Validate email
        if 'email' in data:
            if not isinstance(data['email'], str) or not self.validate_email(data['email']):
                errors.append("Invalid email format")
        
        # Validate age
        if 'age' in data:
            if data['age'] is not None:
                if not isinstance(data['age'], int) or data['age'] < 0 or data['age'] > 150:
                    errors.append("Age must be an integer between 0 and 150")
        
        # Check for unexpected fields
        allowed_fields = ['name', 'email', 'age']
        for field in data:
            if field not in allowed_fields:
                errors.append(f"Unexpected field: {field}")
        
        return errors
    
    def parse_json_safely(self, content_length):
        """Safely parse JSON with comprehensive error handling"""
        try:
            if content_length == 0:
                return None, ["Request body is empty"]
            
            if content_length > 10000:  # 10KB limit
                return None, ["Request body too large (max 10KB)"]
            
            post_data = self.rfile.read(content_length)
            
            if not post_data:
                return None, ["Request body is empty"]
            
            # Decode and parse JSON
            json_str = post_data.decode('utf-8')
            data = json.loads(json_str)
            
            if not isinstance(data, dict):
                return None, ["Request body must be a JSON object"]
            
            return data, []
            
        except UnicodeDecodeError:
            return None, ["Invalid UTF-8 encoding in request body"]
        except json.JSONDecodeError as e:
            return None, [f"Invalid JSON format: {str(e)}"]
        except Exception as e:
            return None, [f"Error parsing request: {str(e)}"]
    
    def parse_path(self):
        """Enhanced path parsing with query parameters"""
        url_parts = urllib.parse.urlparse(self.path)
        path_parts = url_parts.path.strip('/').split('/')
        query_params = urllib.parse.parse_qs(url_parts.query)
        
        if len(path_parts) == 1 and path_parts[0] == 'users':
            return 'users', None, query_params
        elif len(path_parts) == 2 and path_parts[0] == 'users':
            try:
                user_id = int(path_parts[1])
                return 'users', user_id, query_params
            except ValueError:
                return None, None, query_params
        return None, None, query_params
    
    def do_GET(self):
        """Enhanced GET with filtering and pagination"""
        resource, user_id, query_params = self.parse_path()
        
        if resource == 'users':
            if user_id is None:
                # GET /users with optional filtering
                users_list = list(self.users.values())
                
                # Apply name filter if provided
                if 'name' in query_params:
                    name_filter = query_params['name'][0].lower()
                    users_list = [u for u in users_list if name_filter in u['name'].lower()]
                
                # Apply age filter if provided
                if 'min_age' in query_params:
                    try:
                        min_age = int(query_params['min_age'][0])
                        users_list = [u for u in users_list if u.get('age') and u['age'] >= min_age]
                    except ValueError:
                        self.send_json_response(400, {
                            "error": "Invalid min_age parameter"
                        })
                        return
                
                # Simple pagination
                page = 1
                per_page = 10
                if 'page' in query_params:
                    try:
                        page = int(query_params['page'][0])
                    except ValueError:
                        page = 1
                
                if 'per_page' in query_params:
                    try:
                        per_page = min(int(query_params['per_page'][0]), 100)  # Max 100 per page
                    except ValueError:
                        per_page = 10
                
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                paginated_users = users_list[start_idx:end_idx]
                
                self.send_json_response(200, {
                    "users": paginated_users,
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": len(users_list),
                        "total_pages": (len(users_list) + per_page - 1) // per_page
                    }
                })
            else:
                # GET /users/{id}
                if user_id in self.users:
                    self.send_json_response(200, {
                        "user": self.users[user_id]
                    })
                else:
                    self.send_json_response(404, {
                        "error": f"User with ID {user_id} not found"
                    })
        else:
            self.send_json_response(404, {
                "error": "Resource not found",
                "available_endpoints": [
                    "GET /users - Get all users (supports ?name=filter&min_age=N&page=N&per_page=N)",
                    "GET /users/{id} - Get specific user",
                    "POST /users - Create new user",
                    "PUT /users/{id} - Update existing user",
                    "DELETE /users/{id} - Delete user"
                ]
            })
    
    def do_POST(self):
        """Enhanced POST with comprehensive validation"""
        resource, user_id, _ = self.parse_path()
        
        if resource == 'users' and user_id is None:
            content_length = int(self.headers.get('Content-Length', 0))
            user_data, parse_errors = self.parse_json_safely(content_length)
            
            if parse_errors:
                self.send_json_response(400, {
                    "error": "JSON parsing failed",
                    "details": parse_errors
                })
                return
            
            # Validate user data
            validation_errors = self.validate_user_data(user_data, is_update=False)
            if validation_errors:
                self.send_json_response(400, {
                    "error": "Validation failed",
                    "details": validation_errors
                })
                return
            
            # Check for duplicate email
            for existing_user in self.users.values():
                if existing_user['email'].lower() == user_data['email'].lower():
                    self.send_json_response(409, {
                        "error": "Email already exists",
                        "details": ["A user with this email address already exists"]
                    })
                    return
            
            # Create new user
            new_user = {
                "id": self.next_id,
                "name": user_data['name'].strip(),
                "email": user_data['email'].lower(),
                "age": user_data.get('age'),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            self.users[self.next_id] = new_user
            self.next_id += 1
            
            self.send_json_response(201, {
                "message": "User created successfully",
                "user": new_user
            })
        else:
            self.send_json_response(405, {
                "error": "Method not allowed for this endpoint"
            })
    
    def do_PUT(self):
        """Enhanced PUT with validation"""
        resource, user_id, _ = self.parse_path()
        
        if resource == 'users' and user_id is not None:
            if user_id not in self.users:
                self.send_json_response(404, {
                    "error": f"User with ID {user_id} not found"
                })
                return
            
            content_length = int(self.headers.get('Content-Length', 0))
            update_data, parse_errors = self.parse_json_safely(content_length)
            
            if parse_errors:
                self.send_json_response(400, {
                    "error": "JSON parsing failed",
                    "details": parse_errors
                })
                return
            
            # Validate update data
            validation_errors = self.validate_user_data(update_data, is_update=True)
            if validation_errors:
                self.send_json_response(400, {
                    "error": "Validation failed",
                    "details": validation_errors
                })
                return
            
            # Check for duplicate email (excluding current user)
            if 'email' in update_data:
                for uid, existing_user in self.users.items():
                    if uid != user_id and existing_user['email'].lower() == update_data['email'].lower():
                        self.send_json_response(409, {
                            "error": "Email already exists",
                            "details": ["Another user with this email address already exists"]
                        })
                        return
            
            # Update user
            user = self.users[user_id]
            if 'name' in update_data:
                user['name'] = update_data['name'].strip()
            if 'email' in update_data:
                user['email'] = update_data['email'].lower()
            if 'age' in update_data:
                user['age'] = update_data['age']
            
            user['updated_at'] = datetime.now().isoformat()
            
            self.send_json_response(200, {
                "message": "User updated successfully",
                "user": user
            })
        else:
            self.send_json_response(405, {
                "error": "Method not allowed or invalid endpoint"
            })
    
    def do_DELETE(self):
        """Enhanced DELETE with confirmation"""
        resource, user_id, _ = self.parse_path()
        
        if resource == 'users' and user_id is not None:
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

def run_server(port=8000):
    """Start the advanced API server"""
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, AdvancedAPIHandler)
    print(f"Advanced RESTful API Server running on http://localhost:{port}")
    print("Enhanced features:")
    print("  - Comprehensive JSON validation")
    print("  - Email format validation")
    print("  - Duplicate email prevention")
    print("  - Query parameter filtering")
    print("  - Basic pagination")
    print("  - Detailed error messages")
    print("  - Timestamps for all operations")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()

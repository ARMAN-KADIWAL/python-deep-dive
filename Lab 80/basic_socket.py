"""
Basic Socket Creation Example
This script demonstrates how to create a socket object
"""

import socket
import sys

def create_basic_socket():
    """Create and display basic socket information"""
    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created successfully!")
        print(f"Socket family: {sock.family}")
        print(f"Socket type: {sock.type}")
        print(f"Socket protocol: {sock.proto}")


        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"Local IP: {local_ip}")


        sock.close()
        print("Socket closed successfully!")

    except socket.error as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_basic_socket()

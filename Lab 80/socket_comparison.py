"""
Socket Type Comparison
Demonstrates differences between TCP and UDP
"""

import socket
import time

def tcp_example():
    """Demonstrate TCP socket characteristics"""
    print("=== TCP (SOCK_STREAM) Example ===")


    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"TCP Socket Type: {tcp_socket.type}")
    print("TCP Characteristics:")
    print("- Connection-oriented")
    print("- Reliable data delivery")
    print("- Ordered data transmission")
    print("- Error checking and correction")
    print("- Stream reliability adds protocol overhead; performance depends on workload")

    tcp_socket.close()
    print()

def udp_example():
    """Demonstrate UDP socket characteristics"""
    print("=== UDP (SOCK_DGRAM) Example ===")


    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"UDP Socket Type: {udp_socket.type}")
    print("UDP Characteristics:")
    print("- Connectionless")
    print("- No delivery guarantee")
    print("- No order guarantee")
    print("- Minimal error checking")
    print("- Datagram overhead is lower; application performance depends on workload")

    udp_socket.close()
    print()

def socket_options_demo():
    """Demonstrate common socket options"""
    print("=== Socket Options Demo ===")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    reuse_addr = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    recv_buffer = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    send_buffer = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

    print(f"SO_REUSEADDR: {reuse_addr}")
    print(f"Receive Buffer Size: {recv_buffer} bytes")
    print(f"Send Buffer Size: {send_buffer} bytes")


    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("SO_REUSEADDR enabled")

    sock.close()

if __name__ == "__main__":
    tcp_example()
    udp_example()
    socket_options_demo()

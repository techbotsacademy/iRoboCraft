import socket
import http.server
import socketserver

ip = socket.gethostbyname(socket.gethostname())
port = 8000

print(f"\nOpen this on the same Wi-Fi:")
print(f"http://{ip}:{port}\n")

socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler).serve_forever()

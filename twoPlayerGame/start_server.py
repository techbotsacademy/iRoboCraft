import json
import http.server
import socketserver
import socket

ip = socket.gethostbyname(socket.gethostname())
port = 8000

print(f"\nOpen on same Wi-Fi:")
print(f"http://{ip}:{port}\n")

# Shared game state
STATE = {
    "paddle1": 150,
    "paddle2": 150
}

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/update":
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))

            if "paddle1" in data:
                STATE["paddle1"] = data["paddle1"]
            if "paddle2" in data:
                STATE["paddle2"] = data["paddle2"]

            self.send_response(200)
            self.end_headers()

    def do_GET(self):
        if self.path == "/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(STATE).encode())
        else:
            super().do_GET()

socketserver.TCPServer(("", port), Handler).serve_forever()

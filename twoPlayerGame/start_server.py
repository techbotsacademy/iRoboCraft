import http.server
import socketserver
import json

PORT = 8000

WIDTH = 800
HEIGHT = 400
PADDLE_H = 80

# shared state
state = {
    "p1": False,
    "p2": False,
    "p1y": 160,
    "p2y": 160,
    "started": False,
    "ball": {"x": 400, "y": 200, "vx": 2, "vy": 1.5},
    "running": True,
    "winner": ""
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/state":
            if state["started"] and state["running"]:
                self.update_ball()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(state).encode())
            return
        super().do_GET()

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))

        if data["type"] == "join":
            state[data["player"]] = True
            if state["p1"] and state["p2"]:
                state["started"] = True

        if data["type"] == "move" and state["running"]:
            state[data["player"] + "y"] += data["dy"]
            # clamp paddle
            state[data["player"] + "y"] = max(0, min(HEIGHT - PADDLE_H, state[data["player"] + "y"]))

        self.send_response(200)
        self.end_headers()

    def update_ball(self):
        ball = state["ball"]
        ball["x"] += ball["vx"]
        ball["y"] += ball["vy"]

        # bounce top/bottom
        if ball["y"] < 0 or ball["y"] > HEIGHT:
            ball["vy"] *= -1

        # paddle collisions
        if ball["x"] <= 20 and state["p1y"] <= ball["y"] <= state["p1y"] + PADDLE_H:
            ball["vx"] *= -1
        elif ball["x"] <= 0:
            state["running"] = False
            state["winner"] = "Player 2"

        if ball["x"] >= WIDTH - 20 and state["p2y"] <= ball["y"] <= state["p2y"] + PADDLE_H:
            ball["vx"] *= -1
        elif ball["x"] >= WIDTH:
            state["running"] = False
            state["winner"] = "Player 1"

socketserver.TCPServer(("", PORT), Handler).serve_forever()

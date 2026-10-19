import http.server
import socketserver
import json
import time
import threading
import os

PORT = 8000

WIDTH = 800
HEIGHT = 400
PADDLE_H = 80
BALL_RADIUS = 6

# Shared game state
state = {
    "p1": False,
    "p2": False,
    "p1y": 160,
    "p2y": 160,
    "started": False,
    "countdown": 0,
    "start_time": None,
    "ball": {
        "x": 400,
        "y": 200,
        "vx": 2,
        "vy": 1.5
    },
    "running": True,
    "winner": ""
}

game_lock = threading.Lock()


def reset_game():
    """Reset the game without restarting the Python server."""
    state.update({
        "p1": False,
        "p2": False,
        "p1y": 160,
        "p2y": 160,
        "started": False,
        "countdown": 0,
        "start_time": None,
        "ball": {
            "x": 400,
            "y": 200,
            "vx": 2,
            "vy": 1.5
        },
        "running": True,
        "winner": ""
    })


def update_countdown():
    """Update the five-second countdown."""
    if state["started"] and state["running"]:
        if state["start_time"] is not None:
            elapsed = time.time() - state["start_time"]
            remaining = 5 - int(elapsed)

            state["countdown"] = max(0, remaining)


def update_ball():
    """Move the ball and check wall and paddle collisions."""
    ball = state["ball"]

    old_x = ball["x"]

    ball["x"] += ball["vx"]
    ball["y"] += ball["vy"]

    # Bounce off top and bottom edges.
    if ball["y"] - BALL_RADIUS <= 0:
        ball["y"] = BALL_RADIUS
        ball["vy"] = abs(ball["vy"])

    elif ball["y"] + BALL_RADIUS >= HEIGHT:
        ball["y"] = HEIGHT - BALL_RADIUS
        ball["vy"] = -abs(ball["vy"])

    # Player 1 paddle collision.
    p1_top = state["p1y"]
    p1_bottom = p1_top + PADDLE_H

    if (
        ball["vx"] < 0
        and old_x - BALL_RADIUS > 20
        and ball["x"] - BALL_RADIUS <= 20
        and p1_top <= ball["y"] <= p1_bottom
    ):
        ball["x"] = 20 + BALL_RADIUS
        ball["vx"] = abs(ball["vx"])

    # Player 2 paddle collision.
    p2_top = state["p2y"]
    p2_bottom = p2_top + PADDLE_H

    if (
        ball["vx"] > 0
        and old_x + BALL_RADIUS < WIDTH - 20
        and ball["x"] + BALL_RADIUS >= WIDTH - 20
        and p2_top <= ball["y"] <= p2_bottom
    ):
        ball["x"] = WIDTH - 20 - BALL_RADIUS
        ball["vx"] = -abs(ball["vx"])

    # Player 2 wins if the ball passes Player 1.
    if ball["x"] + BALL_RADIUS < 0:
        state["running"] = False
        state["winner"] = "Player 2"

    # Player 1 wins if the ball passes Player 2.
    elif ball["x"] - BALL_RADIUS > WIDTH:
        state["running"] = False
        state["winner"] = "Player 1"


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/state":
            with game_lock:
                update_countdown()

                # Start moving the ball only after countdown ends.
                if (
                    state["started"]
                    and state["running"]
                    and state["countdown"] <= 0
                ):
                    update_ball()

                response = {
                    key: value
                    for key, value in state.items()
                    if key != "start_time"
                }

            body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type", "application/json; charset=utf-8"
            )
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # Serve index.html and other local files normally.
        super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))

        try:
            data = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_error(400, "Invalid JSON")
            return

        with game_lock:
            update_countdown()
            action = data.get("type")

            if action == "join":
                player = data.get("player")

                if (
                    player in ("p1", "p2")
                    and not state["started"]
                    and not state[player]
                ):
                    state[player] = True

                    # Start countdown when both players have joined.
                    if state["p1"] and state["p2"]:
                        state["started"] = True
                        state["running"] = True
                        state["countdown"] = 5
                        state["start_time"] = time.time()

            elif action == "move":
                player = data.get("player")
                dy = data.get("dy")

                if (
                    player in ("p1", "p2")
                    and isinstance(dy, int)
                    and not isinstance(dy, bool)
                    and abs(dy) <= 10
                    and state["started"]
                    and state["running"]
                    and state["countdown"] <= 0
                ):
                    key = player + "y"
                    state[key] = max(
                        0,
                        min(HEIGHT - PADDLE_H, state[key] + dy)
                    )

            elif action == "restart":
                reset_game()

        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()


# Allow quick server restarts during development.
class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with ReusableTCPServer(("", PORT), Handler) as server:
        print("LAN Ping Pong server running on port", PORT)
        print("Open http://localhost:8000")
        server.serve_forever()
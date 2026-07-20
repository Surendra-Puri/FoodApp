import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
STATIC_DIR = Path(__file__).resolve().parent / "static"

items = {
    1: {"id": 1, "name": "Notebook", "price": 5.99},
    2: {"id": 2, "name": "Pen", "price": 1.49},
}
next_item_id = 3


HOME_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Simple CI/CD Food App</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #f6f7fb; color: #20242c; }
    main { max-width: 960px; margin: 0 auto; padding: 48px 20px; }
    h1 { margin: 0 0 10px; font-size: 36px; }
    p { margin: 0 0 28px; color: #566070; font-size: 17px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }
    .card {
      background: white;
      border: 1px solid #dfe3ea;
      border-radius: 8px;
      color: inherit;
      display: block;
      padding: 22px;
      text-decoration: none;
      box-shadow: 0 8px 24px rgba(32, 36, 44, 0.08);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .card:hover { box-shadow: 0 12px 28px rgba(32, 36, 44, 0.14); transform: translateY(-2px); }
    .card img { width: 100%; height: 180px; object-fit: contain; display: block; margin-bottom: 16px; }
    .card h2 { margin: 0 0 8px; font-size: 22px; }
    .status {
      display: inline-block;
      margin-top: 28px;
      padding: 10px 14px;
      background: #e7f7ed;
      border: 1px solid #b7e2c4;
      border-radius: 8px;
      color: #186534;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <main>
    <h1>Simple CI/CD Food App</h1>
    <p>Use this tiny visual app to test GitHub Actions, Docker, ACR, and AKS deployments.</p>

    <section class="grid" aria-label="Food cards">
      <a class="card" href="/pizza">
        <img src="/static/pizza.svg" alt="Pizza slice">
        <h2>Pizza Pod</h2>
        <p>Click to see three pizza types.</p>
      </a>

      <a class="card" href="/cake">
        <img src="/static/cake.svg" alt="Layer cake">
        <h2>Cake Service</h2>
        <p>Click to see three cake types.</p>
      </a>
    </section>

    <div class="status">Health endpoint: /health</div>
  </main>
</body>
</html>
"""

PIZZA_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pizza Types</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #fff7ed; color: #20242c; }
    main { max-width: 960px; margin: 0 auto; padding: 48px 20px; }
    h1 { margin: 0 0 10px; font-size: 36px; }
    p { margin: 0 0 28px; color: #566070; font-size: 17px; }
    .back { display: inline-block; margin-bottom: 24px; color: #a04412; font-weight: 700; text-decoration: none; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; }
    .card { background: white; border: 1px solid #ead8c5; border-radius: 8px; padding: 22px; box-shadow: 0 8px 24px rgba(32, 36, 44, 0.08); }
    .emoji { font-size: 56px; margin-bottom: 14px; }
    h2 { margin: 0 0 8px; font-size: 22px; }
  </style>
</head>
<body>
  <main>
    <a class="back" href="/">Back to menu</a>
    <h1>3 Pizza Types</h1>
    <p>Choose your deployment flavor.</p>

    <section class="grid" aria-label="Pizza types">
      <article class="card"><div class="emoji">Pizza</div><h2>Margherita</h2><p>Classic tomato, mozzarella, and basil.</p></article>
      <article class="card"><div class="emoji">Cheese</div><h2>Cheese Burst</h2><p>Extra cheese for a richer rollout.</p></article>
      <article class="card"><div class="emoji">Spicy</div><h2>Spicy Veggie</h2><p>Peppers, onions, olives, and heat.</p></article>
    </section>
  </main>
</body>
</html>
"""

CAKE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cake Types</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #f5f3ff; color: #20242c; }
    main { max-width: 960px; margin: 0 auto; padding: 48px 20px; }
    h1 { margin: 0 0 10px; font-size: 36px; }
    p { margin: 0 0 28px; color: #566070; font-size: 17px; }
    .back { display: inline-block; margin-bottom: 24px; color: #6b21a8; font-weight: 700; text-decoration: none; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; }
    .card { background: white; border: 1px solid #ddd6fe; border-radius: 8px; padding: 22px; box-shadow: 0 8px 24px rgba(32, 36, 44, 0.08); }
    .emoji { font-size: 56px; margin-bottom: 14px; }
    h2 { margin: 0 0 8px; font-size: 22px; }
  </style>
</head>
<body>
  <main>
    <a class="back" href="/">Back to menu</a>
    <h1>3 Cake Types</h1>
    <p>Sweet options from your running app.</p>

    <section class="grid" aria-label="Cake types">
      <article class="card"><div class="emoji">Cake</div><h2>Strawberry Cake</h2><p>Soft layers with berry frosting.</p></article>
      <article class="card"><div class="emoji">Party</div><h2>Birthday Cake</h2><p>Colorful, cheerful, and celebration-ready.</p></article>
      <article class="card"><div class="emoji">Cocoa</div><h2>Chocolate Cake</h2><p>Rich cocoa layers with creamy icing.</p></article>
    </section>
  </main>
</body>
</html>
"""


class RestApiHandler(BaseHTTPRequestHandler):
    def _send_html(self, status_code, html):
        body = html.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status_code, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_static_svg(self, filename):
        path = STATIC_DIR / filename
        if not path.exists():
            self._send_json(404, {"error": "Asset not found"})
            return

        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}

        body = self.rfile.read(content_length).decode("utf-8")
        return json.loads(body)

    def _item_id_from_path(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "items" and parts[1].isdigit():
            return int(parts[1])
        return None

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self._send_html(200, HOME_HTML)
            return

        if path == "/pizza":
            self._send_html(200, PIZZA_HTML)
            return

        if path == "/cake":
            self._send_html(200, CAKE_HTML)
            return

        if path == "/static/pizza.svg":
            self._send_static_svg("pizza.svg")
            return

        if path == "/static/cake.svg":
            self._send_static_svg("cake.svg")
            return

        if path == "/health":
            self._send_json(200, {"status": "ok"})
            return

        if path == "/items":
            self._send_json(200, list(items.values()))
            return

        item_id = self._item_id_from_path()
        if item_id is not None:
            item = items.get(item_id)
            if item is None:
                self._send_json(404, {"error": "Item not found"})
                return
            self._send_json(200, item)
            return

        self._send_json(404, {"error": "Route not found"})

    def do_POST(self):
        global next_item_id

        if urlparse(self.path).path != "/items":
            self._send_json(404, {"error": "Route not found"})
            return

        try:
            data = self._read_json()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        name = data.get("name")
        price = data.get("price")
        if not name or price is None:
            self._send_json(400, {"error": "Fields 'name' and 'price' are required"})
            return

        item = {"id": next_item_id, "name": name, "price": price}
        items[next_item_id] = item
        next_item_id += 1
        self._send_json(201, item)

    def do_PUT(self):
        item_id = self._item_id_from_path()
        if item_id is None:
            self._send_json(404, {"error": "Route not found"})
            return

        if item_id not in items:
            self._send_json(404, {"error": "Item not found"})
            return

        try:
            data = self._read_json()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        if "name" in data:
            items[item_id]["name"] = data["name"]
        if "price" in data:
            items[item_id]["price"] = data["price"]

        self._send_json(200, items[item_id])

    def do_DELETE(self):
        item_id = self._item_id_from_path()
        if item_id is None:
            self._send_json(404, {"error": "Route not found"})
            return

        deleted_item = items.pop(item_id, None)
        if deleted_item is None:
            self._send_json(404, {"error": "Item not found"})
            return

        self._send_json(200, {"deleted": deleted_item})


def run_server():
    server = ThreadingHTTPServer((HOST, PORT), RestApiHandler)
    print(f"REST API running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

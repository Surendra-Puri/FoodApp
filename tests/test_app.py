import json
import socket
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from app import RestApiHandler


class QuietRestApiHandler(RestApiHandler):
    def log_message(self, format, *args):
        return


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = free_port()
        cls.server = ThreadingHTTPServer(("127.0.0.1", cls.port), QuietRestApiHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def request(self, method, path, body=None):
        conn = HTTPConnection("127.0.0.1", self.port)
        payload = json.dumps(body) if body is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        conn.request(method, path, body=payload, headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()
        return response.status, data

    def test_health_endpoint(self):
        status, body = self.request("GET", "/health")

        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"status": "ok"})

    def test_home_page(self):
        status, body = self.request("GET", "/")

        self.assertEqual(status, 200)
        self.assertIn("Pizza Pod", body)
        self.assertIn("Cake Service", body)

    def test_food_pages(self):
        pizza_status, pizza_body = self.request("GET", "/pizza")
        cake_status, cake_body = self.request("GET", "/cake")

        self.assertEqual(pizza_status, 200)
        self.assertIn("Margherita", pizza_body)
        self.assertEqual(cake_status, 200)
        self.assertIn("Chocolate Cake", cake_body)


if __name__ == "__main__":
    unittest.main()

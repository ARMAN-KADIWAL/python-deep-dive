"""Run a real CRUD integration test against an ephemeral loopback server."""
import json
import threading
import unittest
from http.server import HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from restful_api import RESTfulAPIHandler


class RestfulAPITests(unittest.TestCase):
    def test_crud_and_unique_ids(self):
        RESTfulAPIHandler.users = {}
        RESTfulAPIHandler.next_id = 1
        server = HTTPServer(("127.0.0.1", 0), RESTfulAPIHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(thread.join, 3)
        self.addCleanup(server.shutdown)
        base = f"http://127.0.0.1:{server.server_port}"

        def request(method, path, payload=None):
            body = None if payload is None else json.dumps(payload).encode()
            req = Request(base + path, data=body, method=method,
                          headers={"Content-Type": "application/json"})
            try:
                with urlopen(req, timeout=5) as response:
                    return response.status, json.load(response)
            except HTTPError as response:
                with response:
                    return response.code, json.load(response)

        status, first = request("POST", "/users", {"name": "A", "email": "a@example.com"})
        self.assertEqual(status, 201)
        status, second = request("POST", "/users", {"name": "B", "email": "b@example.com"})
        self.assertEqual(status, 201)
        first_id, second_id = first["user"]["id"], second["user"]["id"]
        self.assertNotEqual(first_id, second_id)
        self.assertEqual(request("GET", "/users")[1]["total"], 2)
        self.assertEqual(request("PUT", f"/users/{first_id}", {"name": "Updated"})[0], 200)
        self.assertEqual(request("GET", f"/users/{first_id}")[1]["name"], "Updated")
        self.assertEqual(request("DELETE", f"/users/{first_id}")[0], 200)
        self.assertEqual(request("GET", f"/users/{first_id}")[0], 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)

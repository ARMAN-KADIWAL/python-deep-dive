import unittest

import app as lab


class RestApiTests(unittest.TestCase):
    def setUp(self):
        self.client = lab.app.test_client()
        lab.items_data[:] = [
            {"id": 1, "name": "Laptop", "category": "Electronics",
             "price": 999.99, "created_at": "2024-01-01T10:00:00Z"},
            {"id": 2, "name": "Book", "category": "Education",
             "price": 29.99, "created_at": "2024-01-02T11:30:00Z"},
        ]
        lab.next_id = 3

    def test_index_and_get(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/api/items").json["count"], 2)
        self.assertEqual(self.client.get("/api/items/1").json["data"]["name"], "Laptop")
        self.assertEqual(self.client.get("/api/items/999").status_code, 404)

    def test_post_validation_and_creation(self):
        self.assertEqual(self.client.post("/api/items", json={}).status_code, 400)
        self.assertEqual(self.client.post("/api/items", data="{broken",
                         content_type="application/json").status_code, 400)
        self.assertEqual(self.client.post("/api/items", json={
            "name": "Bad", "category": "Test", "price": -1,
        }).status_code, 400)
        result = self.client.post("/api/items", json={
            "name": "Mouse", "category": "Electronics", "price": 25,
        })
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.json["data"]["id"], 3)

    def test_list_and_statistics(self):
        result = self.client.get(
            "/api/items/list?category=electronics&sort_by=price&order=desc&limit=1")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json["count"], 1)
        self.assertEqual(result.json["data"][0]["name"], "Laptop")
        self.assertEqual(self.client.get("/api/items/list?sort_by=unknown").status_code, 400)
        stats = self.client.get("/api/items/stats")
        self.assertEqual(stats.json["statistics"]["total_items"], 2)
        self.assertEqual(stats.json["statistics"]["total_value"], 1029.98)


if __name__ == "__main__":
    unittest.main()

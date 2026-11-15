"""Lab 66: RESTful API with GET, POST, filtering, sorting, and statistics."""

import math
import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Lab-only in-memory data: changes are lost when the server restarts.
items_data = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99,
     "created_at": "2024-01-01T10:00:00Z"},
    {"id": 2, "name": "Book", "category": "Education", "price": 29.99,
     "created_at": "2024-01-02T11:30:00Z"},
]
next_id = 3


def error(message, status=400):
    return {"status": "error", "message": message}, status


class ItemAPI(Resource):
    def get(self, item_id=None):
        if item_id is None:
            return {"status": "success", "data": items_data, "count": len(items_data)}, 200
        item = next((row for row in items_data if row["id"] == item_id), None)
        if item is None:
            return error("Item not found", 404)
        return {"status": "success", "data": item}, 200

    def post(self, item_id=None):
        global next_id
        if item_id is not None:
            return error("Create items at /api/items", 405)
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return error("A valid JSON object is required")
        for field in ("name", "category", "price"):
            if field not in data:
                return error(f"Missing required field: {field}")
        if not isinstance(data["name"], str) or not data["name"].strip():
            return error("name must be non-empty text")
        if not isinstance(data["category"], str) or not data["category"].strip():
            return error("category must be non-empty text")
        if isinstance(data["price"], bool):
            return error("price must be a non-negative number")
        try:
            price = float(data["price"])
        except (TypeError, ValueError, OverflowError):
            return error("price must be a non-negative number")
        if not math.isfinite(price) or price < 0:
            return error("price must be a non-negative number")

        item = {
            "id": next_id,
            "name": data["name"].strip(),
            "category": data["category"].strip(),
            "price": round(price, 2),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        items_data.append(item)
        next_id += 1
        return {"status": "success", "message": "Item created successfully", "data": item}, 201


class ItemListAPI(Resource):
    def get(self):
        category = request.args.get("category", "").strip()
        sort_by = request.args.get("sort_by", "id")
        order = request.args.get("order", "asc").lower()
        limit = request.args.get("limit", type=int)

        if sort_by not in {"id", "name", "category", "price"}:
            return error("Invalid sort_by field")
        if order not in {"asc", "desc"}:
            return error("order must be asc or desc")
        if "limit" in request.args and (limit is None or limit <= 0):
            return error("limit must be a positive integer")

        rows = [
            row.copy() for row in items_data
            if not category or row["category"].casefold() == category.casefold()
        ]
        rows.sort(key=lambda row: row[sort_by], reverse=(order == "desc"))
        if limit is not None:
            rows = rows[:limit]
        return {
            "status": "success",
            "data": rows,
            "count": len(rows),
            "filters_applied": {
                "category": category or None,
                "sort_by": sort_by,
                "order": order,
                "limit": limit,
            },
        }, 200


class ItemStatsAPI(Resource):
    def get(self):
        categories = {}
        for row in items_data:
            entry = categories.setdefault(row["category"], {"count": 0, "total_value": 0})
            entry["count"] += 1
            entry["total_value"] = round(entry["total_value"] + row["price"], 2)

        total = round(sum(row["price"] for row in items_data), 2)
        return {
            "status": "success",
            "statistics": {
                "total_items": len(items_data),
                "total_value": total,
                "average_price": round(total / len(items_data), 2) if items_data else 0,
                "categories": categories,
                "most_expensive_item": max(items_data, key=lambda row: row["price"])
                if items_data else None,
            },
        }, 200


# Register exact/static paths as well as the parameterized item lookup.
api.add_resource(ItemListAPI, "/api/items/list")
api.add_resource(ItemStatsAPI, "/api/items/stats")
api.add_resource(ItemAPI, "/api/items", "/api/items/<int:item_id>")


@app.get("/")
def home():
    return jsonify({
        "message": "Flask RESTful API Lab 66",
        "endpoints": [
            "GET /api/items",
            "GET /api/items/1",
            "POST /api/items",
            "GET /api/items/list?category=Electronics&sort_by=price&order=desc&limit=2",
            "GET /api/items/stats",
        ],
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)

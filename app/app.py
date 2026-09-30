from flask import Flask, request, jsonify
import os

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", "8080"))

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 75000,
        "category": "Electronics"
    },
    {
        "id": 2,
        "name": "Mobile Phone",
        "price": 30000,
        "category": "Electronics"
    }
]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "environment": APP_ENV
    }), 200


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({
            "error": "name and price are required"
        }), 400

    new_product = {
        "id": max([product["id"] for product in products], default=0) + 1,
        "name": data["name"],
        "price": data["price"],
        "category": data.get("category", "General")
    }

    products.append(new_product)

    return jsonify(new_product), 201


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    if "name" in data:
        product["name"] = data["name"]

    if "price" in data:
        product["price"] = data["price"]

    if "category" in data:
        product["category"] = data["category"]

    return jsonify(product), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    products.remove(product)

    return jsonify({
        "message": "Product deleted successfully"
    }), 200


if __name__ == "__main__":
    print(f"Starting Product API")
    print(f"Environment: {APP_ENV}")
    print(f"Database Host: {DB_HOST}")
    print(f"Application Port: {APP_PORT}")

    app.run(
        host="0.0.0.0",
        port=APP_PORT
    )
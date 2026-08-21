from flask import Flask, request, jsonify
from database import init_db, get_connection

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return "Expense tracker is running!"

@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description", "")
    date = data.get("date")

    if amount is None or category is None or date is None:
        return jsonify({"error": "amount, category, and date are required"}), 400

    if not isinstance(amount, (int, float)):
        return jsonify({"error": "amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"error": "amount must be greater than 0"}), 400

    if not isinstance(category, str) or category.strip() == "":
        return jsonify({"error": "category must be a non-empty string"}), 400

    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
        (amount, category, description, date)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"}), 201

@app.route("/expenses", methods=["GET"])
def get_expenses():
    category = request.args.get("category")

    conn = get_connection()
    if category:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE category = ?", (category,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    expenses = [dict(row) for row in rows]
    return jsonify(expenses), 200

if __name__ == "__main__":
    app.run(debug=True)

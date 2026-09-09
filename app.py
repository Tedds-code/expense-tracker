from flask import Flask, request, jsonify, render_template
from database import init_db, get_connection

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("index.html")

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
    year = request.args.get("year")
    month = request.args.get("month")
    day = request.args.get("day")

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if year:
        query += " AND strftime('%Y', date) = ?"
        params.append(year.zfill(4))

    if month:
        query += " AND strftime('%m', date) = ?"
        params.append(month.zfill(2))

    if day:
        query += " AND strftime('%d', date) = ?"
        params.append(day.zfill(2))

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    expenses = [dict(row) for row in rows]
    return jsonify(expenses), 200

@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    conn = get_connection()
    result = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({"message": "Expense deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)

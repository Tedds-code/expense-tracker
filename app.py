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

    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description", "")
    date = data.get("date")

    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
        (amount, category, description, date)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)

import os
import pytest

os.environ["DATABASE_NAME"] = "test_expenses.db"

from app import app
from database import init_db


@pytest.fixture
def client():
    init_db()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

    if os.path.exists("test_expenses.db"):
        os.remove("test_expenses.db")


def test_add_expense_success(client):
    response = client.post("/expenses", json={
        "amount": 20.5,
        "category": "food",
        "description": "Groceries",
        "date": "2026-08-21"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Expense added successfully"


def test_add_expense_missing_fields(client):
    response = client.post("/expenses", json={"amount": 20.5})
    assert response.status_code == 400


def test_add_expense_negative_amount(client):
    response = client.post("/expenses", json={
        "amount": -5,
        "category": "food",
        "date": "2026-08-21"
    })
    assert response.status_code == 400


def test_get_expenses_empty(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_expenses_after_adding(client):
    client.post("/expenses", json={
        "amount": 15,
        "category": "transport",
        "date": "2026-08-20"
    })
    response = client.get("/expenses")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["category"] == "transport"


def test_filter_by_category(client):
    client.post("/expenses", json={"amount": 10, "category": "food", "date": "2026-08-21"})
    client.post("/expenses", json={"amount": 20, "category": "transport", "date": "2026-08-21"})

    response = client.get("/expenses?category=food")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["category"] == "food"


def test_delete_expense(client):
    post_response = client.post("/expenses", json={
        "amount": 10, "category": "food", "date": "2026-08-21"
    })
    expenses = client.get("/expenses").get_json()
    expense_id = expenses[0]["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 200

    expenses_after = client.get("/expenses").get_json()
    assert len(expenses_after) == 0


def test_delete_nonexistent_expense(client):
    response = client.delete("/expenses/999")
    assert response.status_code == 404

import threading
import webview
from app import app

def run_flask():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    webview.create_window("Expense Tracker", "http://127.0.0.1:5000")
    webview.start()

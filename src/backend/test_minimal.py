"""Minimal Flask test to isolate the issue"""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Minimal Flask test working"}

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("Starting minimal Flask server...")
    app.run(host="0.0.0.0", port=8001, debug=False)
    print("Server stopped")

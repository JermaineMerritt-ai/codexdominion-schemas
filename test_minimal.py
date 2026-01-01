"""Minimal test to verify Flask works"""
from flask import Flask, session as flask_session
app = Flask(__name__)
app.secret_key = 'test-secret'

@app.route('/')
def index():
    return "Flask works!"

@app.route('/test-session')
def test_session():
    flask_session['test'] = 'value'
    return f"Session works! Value: {flask_session.get('test')}"

if __name__ == '__main__':
    print("Starting minimal Flask test...")
    app.run(host='127.0.0.1', port=5001, debug=False)

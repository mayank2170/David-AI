from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'david.db')


def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/contact', methods=['POST'])
def contact():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
                (name, email, message)
            )
            conn.commit()

        return jsonify({"success": True, "message": "Contact saved successfully"}), 201
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

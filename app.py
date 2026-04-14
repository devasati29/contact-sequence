from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    conn = sqlite3.connect('counter.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            value INTEGER
        )
    """)

    # Insert initial value if not exists
    cursor.execute("SELECT COUNT(*) FROM counter")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO counter (value) VALUES (0)")

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Generate Next Contact ID
# -----------------------------
@app.route('/next-id', methods=['GET', 'POST'])
def get_next_id():
    try:
        conn = sqlite3.connect('counter.db')
        cursor = conn.cursor()

        # Atomic increment
        cursor.execute("UPDATE counter SET value = value + 1 WHERE id = 1")
        conn.commit()

        # Fetch updated value
        cursor.execute("SELECT value FROM counter WHERE id = 1")
        new_value = cursor.fetchone()[0]

        conn.close()

        # Format ID → C-0001
        contact_id = f"C-{new_value:04d}"

        return jsonify({
            "status": "success",
            "contact_id": contact_id
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -----------------------------
# Health Check (optional)
# -----------------------------
@app.route('/')
def home():
    return "API is running 🚀"


# -----------------------------
# Run App (Render Compatible)
# -----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
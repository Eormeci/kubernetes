from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_PATH = "/data/database.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# GET /db/ping
# -------------------------
@app.route('/db/ping')
def ping():
    return jsonify({"status": "ok", "message": "DB servisi çalışıyor 🚀"})


# -------------------------
# POST /db/migrate
# -------------------------
@app.route('/db/migrate', methods=['POST'])
def migrate():
    try:
        conn = get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT
            )
        """)
        conn.commit()
        conn.close()
        return jsonify({"migrate": True, "message": "Users tablosu oluşturuldu."})
    except Exception as e:
        return jsonify({"migrate": False, "error": str(e)}), 500


# -------------------------
# CRUD: /db/users
# -------------------------
@app.route('/db/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    conn = get_db()

    # GET → listele
    if request.method == 'GET':
        users = conn.execute("SELECT * FROM users").fetchall()
        return jsonify([dict(u) for u in users])

    data = request.json if request.is_json else {}

    # POST → ekle
    if request.method == 'POST':
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                     (data.get("name"), data.get("email")))
        conn.commit()
        return jsonify({"status": "OK", "message": "Kullanıcı eklendi!"})

    # PUT → güncelle
    if request.method == 'PUT':
        conn.execute("UPDATE users SET name=?, email=? WHERE id=?",
                     (data.get("name"), data.get("email"), data.get("id")))
        conn.commit()
        return jsonify({"status": "OK", "message": "Kullanıcı güncellendi!"})

    # DELETE → sil
    if request.method == 'DELETE':
        conn.execute("DELETE FROM users WHERE id=?", (data.get("id"),))
        conn.commit()
        return jsonify({"status": "OK", "message": "Kullanıcı silindi!"})


@app.route('/')
def root():
    return "DB Servisi ayakta, /db yolunu deneyebilirsin."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)

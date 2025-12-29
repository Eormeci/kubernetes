from flask import Flask, jsonify, request
import subprocess
import psutil
import sqlite3

app = Flask(__name__)

# SQLite veritabanı dosyasını oluştur
DB_FILE = "database.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()

# API başlatıldığında veritabanını başlat
init_db()

@app.route('/api/test')
def hello():
    return jsonify({
        "message": "/api çalışıyor! 🎉",
        "user": "enhar",
        "status": "Success !"
    })

# ============================================================
# CPU BİLGİSİ
# ============================================================
@app.route('/api/cpu')
def cpu_info():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)

        return jsonify({
            "cpu_available": True,
            "usage_percent": cpu_percent,
            "physical_cores": cpu_cores,
            "threads": cpu_threads,
            "frequency_mhz": cpu_freq.current if cpu_freq else None
        })

    except Exception as e:
        return jsonify({
            "cpu_available": False,
            "error": "CPU bilgisi alınamadı.",
            "details": str(e)
        })

# ============================================================
# RAM BİLGİSİ
# ============================================================
@app.route('/api/ram')
def ram_info():
    vm = psutil.virtual_memory()
    return jsonify({
        "total_gb": round(vm.total / (1024 ** 3), 2),
        "used_gb": round(vm.used / (1024 ** 3), 2),
        "free_gb": round(vm.available / (1024 ** 3), 2),
        "percent": vm.percent
    })

# CRUD endpointleri
@app.route('/api/items', methods=['GET'])
def get_items():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        return jsonify([{"id": row[0], "name": row[1], "description": row[2]} for row in items])

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        return jsonify({"id": cursor.lastrowid, "name": name, "description": description}), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET name = ?, description = ? WHERE id = ?", (name, description, item_id))
        conn.commit()
        return jsonify({"id": item_id, "name": name, "description": description})

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return jsonify({"message": "Item deleted successfully."})

@app.route('/')
def root():
    return "API ayakta, /api yolunu dene"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, jsonify
import subprocess
import psutil

app = Flask(__name__)

@app.route('/api')
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


@app.route('/')
def root():
    return "API ayakta, /api yolunu dene"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

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
# 1) GPU BİLGİSİ (Sadece Linux, OS check YOK)
# ============================================================
@app.route('/api/gpu')
def gpu_info():
    try:
        # Sadece Linux'ta çalışacak, direkt nvidia-smi çağırıyoruz.
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"],
            stderr=subprocess.STDOUT,
            text=True
        )

        gpu_list = []
        for line in result.strip().splitlines():
            name, driver, mem = [x.strip() for x in line.split(",")]
            gpu_list.append({
                "name": name,
                "driver": driver,
                "total_memory": mem
            })

        return jsonify({"gpu_available": True, "gpus": gpu_list})

    except Exception as e:
        return jsonify({
            "gpu_available": False,
            "error": "NVIDIA GPU bulunamadı veya nvidia-smi mevcut değil.",
            "details": str(e)
        })


# ============================================================
# 2) RAM BİLGİSİ (Linux için ideal)
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

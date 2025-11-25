from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/api')
def hello():
    return jsonify({
        "message": "ZekaBook API çalışıyor! 🎉",
        "user": "openzeka",
        "status": "çok zeki"
    })

@app.route('/')
def root():
    return "API ayakta, /api yolunu dene"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
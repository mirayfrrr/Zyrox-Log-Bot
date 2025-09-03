import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot çalışıyor!"

def run():
    port = int(os.environ.get("PORT", 8080))  # Render hangi portu verdiyse onu al
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

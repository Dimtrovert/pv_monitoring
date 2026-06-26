from flask import Flask
from config import Config
from database.db import db

# Import Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

# Import MQTT Subscriber
from mqtt.subscriber import start_mqtt

app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi Database
db.init_app(app)

with app.app_context():
    from database.models import PVData, User
    db.create_all()

# Registrasi Blueprint (Menyambungkan rute dari file terpisah)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")

# Rute pengecekan status server
@app.route("/health")
def health():
    return {"status": "online"}

# Nyalakan Mesin Pendengar MQTT (Subscriber)
start_mqtt(app)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
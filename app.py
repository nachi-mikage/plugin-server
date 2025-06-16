# plugin-server/app.py

from flask import Flask
from api.time_api import time_bp
from api.weather_api import weather_bp

app = Flask(__name__)
app.register_blueprint(time_bp)
app.register_blueprint(weather_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

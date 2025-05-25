# backend/app/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def crear_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    # Importar rutas después de crear la app
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

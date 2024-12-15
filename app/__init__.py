from flask import Flask
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    # Konfigurasi Secret Key dan JWT
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Ganti dengan secret key Anda
    jwt = JWTManager(app)
    
    with app.app_context():
        from .routes import bp
        app.register_blueprint(bp)

    return app

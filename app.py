from flask import Flask, render_template, redirect, url_for
from extensions import db, login_manager
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-prod'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fixit.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.client import client_bp
    from routes.worker import worker_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def home():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

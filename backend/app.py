import os
from flask import Flask
from dotenv import load_dotenv
from database import db, migrate
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.reports import reports_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecret')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

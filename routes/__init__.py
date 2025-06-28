from flask import Flask
from models import db, migrate
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from config import Config

login_manager = LoginManager()
oauth = OAuth()

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    oauth.init_app(app)

    login_manager.login_view = 'authapp.login'
    login_manager.login_message = "Anda harus login untuk mengakses halaman ini."
    login_manager.login_message_category = "warning"

    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import authapp
    from .user import userapp
    from .kategori import kategoriapp
    from .barang import barangapp

    app.register_blueprint(authapp)
    app.register_blueprint(userapp)
    app.register_blueprint(kategoriapp)
    app.register_blueprint(barangapp)

    return app
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import db
from models.user import User

from routes.auth import authapp
from routes.barang import barangapp
from routes.kategori import kategoriapp
from routes.user import userapp

from config import Config
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

admin = Admin(app, name='SecureStore Admin')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'authapp.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

with app.app_context():
    db.create_all()

app.register_blueprint(authapp)
app.register_blueprint(barangapp)
app.register_blueprint(kategoriapp)
app.register_blueprint(userapp)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return render_template('login-register.html')

class Controller(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    def not_auth(self):
        return "You are not authorized to access this page.", 403

admin.add_view(ModelView(User, db.session))

if __name__ == '__main__':
    app.run(debug=True)
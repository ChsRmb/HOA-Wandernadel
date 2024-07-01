from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
admin = Admin(name="HOA Wandernadel", template_mode="bootstrap4")
login_manager = LoginManager()
mail = Mail()


def create_dummy_user():
    from app.models import User

    if not User.query.first():
        example = User(username="admin", email="example@example.com", password="admin")
        db.session.add(example)
        db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    #    admin.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail.init_app(app)

    # import blueprints
    from app.routes.main import main as main_bp

    app.register_blueprint(main_bp)
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        create_dummy_user()

        # Configure Admin panel
        from app.admin import setup_admin

    setup_admin(app)

    return app

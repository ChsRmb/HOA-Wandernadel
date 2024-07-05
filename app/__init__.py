from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_mail import Mail
from sqlalchemy import inspect


db = SQLAlchemy()
admin = Admin(name="HOA Wandernadel", template_mode="bootstrap4")
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    #    admin.init_app(app)
    migrate.init_app(app, db)
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
        inspector = inspect(db.engine)
        if not inspector.get_table_names():
            db.create_all()
            from app.tools.dummy_data import create_dummy_data
            create_dummy_data()

        # Configure Admin panel
        from app.admin import setup_admin

    setup_admin(app)

    return app

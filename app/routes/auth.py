from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash

from app import db, mail
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for("admin.index"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth_bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("auth.login"))
    return render_template("reset_password_request.html")


@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        password = request.form.get("password")
        user.password = generate_password_hash(password, method="sha256")
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html")


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message("Password Reset Request", sender=current_app.config["MAIL_USERNAME"], recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)

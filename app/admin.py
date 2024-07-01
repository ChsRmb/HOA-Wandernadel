import logging

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from werkzeug.utils import secure_filename
from wtforms import PasswordField, SelectField
from flask_admin.form import ImageUploadField
from pathlib import Path
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for, current_app

from app import admin, db
from app.models import Location, User, Year


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class UserAdmin(AdminView):
    from_base_class = SecureForm
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]
    form_extra_fields = {"password": PasswordField("Password")}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = form.password.data
        else:
            if form.password.data:
                model.password = form.password.data


class YearAdmin(AdminView):
    column_list = ("id", "year")
    form_columns = ("year",)


class LocationAdmin(AdminView):
    form_base_class = SecureForm
    form_columns = (
        "name",
        "description",
        "latitude",
        "longitude",
        "terrain_level",
        "difficulty_level",
        "image_url",
        "year",
    )

    @staticmethod
    def filename(obj, file_data):
        return secure_filename(Path(file_data.filename).name)

    form_extra_fields = {
        "terrain_level": SelectField("Terrain Level", coerce=int, choices=[(i, str(i)) for i in range(1, 6)]),
        "difficulty_level": SelectField("Difficulty Level", coerce=int, choices=[(i, str(i)) for i in range(1, 6)]),
        "image_url": ImageUploadField(
            "Image", namegen=filename, base_path=Path(current_app.root_path) / "static", relative_path="uploads/"
        ),
    }


def setup_admin(app):
    # admin.init_app(app, index_view=SecureAdminIndexView(template='admin/base.html'))
    admin.init_app(app, index_view=SecureAdminIndexView())
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(LocationAdmin(Location, db.session))
    admin.add_view(YearAdmin(Year, db.session))

from pathlib import Path

from flask import current_app, redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField, ImageUploadField, SecureForm
from flask_login import current_user
from werkzeug.utils import secure_filename
from wtforms import BooleanField, PasswordField, SelectField

from app import admin, db
from app.models import GeneralSettings, Location, LocationType, User, Year


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
    column_list = ("id", "year", "enabled")
    form_columns = ("year", "enabled")
    form_extra_fields = {"enabled": BooleanField("Enabled")}


class LocationTypeAdmin(AdminView):
    form_base_class = SecureForm
    form_columns = ("name", "description")


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
        "enabled",
        "year",
        "loc_type",
    )

    @staticmethod
    def filename(obj, file_data):
        return secure_filename(Path(file_data.filename).name)

    form_extra_fields = {
        "terrain_level": SelectField("Terrain Level", coerce=int, choices=[(i, str(i)) for i in range(1, 6)]),
        "difficulty_level": SelectField("Difficulty Level", coerce=int, choices=[(i, str(i)) for i in range(1, 6)]),
        "enabled": BooleanField("Enabled"),
        "image_url": ImageUploadField(
            "Image", namegen=filename, base_path=Path(current_app.root_path) / "static", relative_path="uploads/"
        ),
    }


class GeneralAdmin(AdminView):
    column_list = (
        "latitude",
        "longitude",
        "zoom_level",
        "marker",
        "marker_width",
        "marker_height",
        "marker_anchor_x",
        "marker_anchor_y",
        "marker_popup_anchor_x",
        "marker_popup_anchor_y",
    )
    form_columns = (
        "latitude",
        "longitude",
        "zoom_level",
        "marker",
        "marker_width",
        "marker_height",
        "marker_anchor_x",
        "marker_anchor_y",
        "marker_popup_anchor_x",
        "marker_popup_anchor_y",
    )
    can_create = False
    can_delete = False
    can_view_details = False

    @staticmethod
    def filename(obj, file_data):
        return secure_filename(Path(file_data.filename).name)

    form_extra_fields = {
        "marker": FileUploadField(
            "Marker",
            namegen=filename,
            base_path=Path(current_app.root_path) / "static",
            relative_path="uploads/",
            allowed_extensions=("png", "jpg", "jpeg", "svg"),
        )
    }

    def scaffold_list_form(self, widget=None, validators=None):
        return self.scaffold_form()

    def get_list(self, *args, **kwargs):
        count, data = super().get_list(*args, **kwargs)
        if count == 0:
            dummy = GeneralSettings(latitude=0.0, longitude=0.0, zoom_level=0)
            db.session.add(dummy)
            db.session.commit()
            return 1, [dummy]
        return count, data


def setup_admin(app):
    # admin.init_app(app, index_view=SecureAdminIndexView(template='admin/base.html'))
    admin.init_app(app, index_view=SecureAdminIndexView())
    admin.add_view(GeneralAdmin(GeneralSettings, db.session))
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(LocationAdmin(Location, db.session))
    admin.add_view(YearAdmin(Year, db.session))
    admin.add_view(LocationTypeAdmin(LocationType, db.session))

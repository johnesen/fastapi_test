from flask_admin.contrib.sqla import ModelView
from flask_admin.form import form
from wtforms import fields

from config.hashing import Hasher


class AdminPasswordField(fields.PasswordField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0] != "":
            self.data = Hasher.hash_password(valuelist[0])
        elif self.data is None:
            self.data = ""


class UserViewCreateForm(form.Form):
    name = fields.StringField("name")
    surname = fields.StringField("surname")
    email = fields.StringField("Email")
    hashed_password = AdminPasswordField("Password")
    is_active = fields.BooleanField("Is Active")
    is_verified = fields.BooleanField("Is Verified")


class UserView(ModelView):
    column_list = ("name", "surname", "email", "hashed_password")
    column_searchable_list = ("name", "email")
    column_filters = ("name", "email")
    form = UserViewCreateForm

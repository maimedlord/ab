from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id_string, email, username, id_object, tz_offset):
        self.email = email
        self.id = id_string
        self.id_object = id_object
        self.username = username
        self.tz_offset = tz_offset


    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def build_user(self):
        return None

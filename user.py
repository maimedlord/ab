from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, username):
        self.email = email
        self.id = id
        self.username = username

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

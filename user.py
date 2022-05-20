from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, username):
        self.id = email
        self.email = email
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


if __name__ == '__main__':
    print("user.py")


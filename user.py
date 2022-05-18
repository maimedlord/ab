from flask_login import UserMixin
import calls


class User(UserMixin):
    def __init__(self, email):
        self.id = email
        self.email = email



    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id


if __name__ == '__main__':
    print("user.py")


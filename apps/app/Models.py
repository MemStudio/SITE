from flask_login import UserMixin

class User(UserMixin):
    id = None
    def __init__(self, usn):
        # в качестве ID пользователя используем `email`
        self.id = usn



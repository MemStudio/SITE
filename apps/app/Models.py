from flask_login import UserMixin
from sqlite3 import *


class User(UserMixin):
    def __init__(self, usn):
        # в качестве ID пользователя используем `email`
        self.id = usn


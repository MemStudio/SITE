import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or ';owieeuiruyoiw6854654eu654687987h'


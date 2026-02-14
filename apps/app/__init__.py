from flask import Flask
from apps.config import Config


app = Flask(__name__)
app.config.from_object(Config)


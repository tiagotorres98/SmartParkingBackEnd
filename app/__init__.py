from urllib.parse import quote_plus

from flask import Flask
from flask_login import LoginManager
from flask_login.utils import login_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import asyncio
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280

import pandas as pd

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.controllers import default
from app.models.tables import User



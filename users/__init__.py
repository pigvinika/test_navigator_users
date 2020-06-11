from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

from users.users_resource import UserListResource, UserAddResource

api.add_resource(UserListResource, '/users')
api.add_resource(UserAddResource, '/users')

# Migration
from users import users_model

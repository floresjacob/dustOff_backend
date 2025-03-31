from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
app.config['CORS_HEADERS'] = 'Content-Type'
# Allow requests from 'http://localhost:5173' 
CORS(app, resources={r"/*": {"origins": "*"}})

# After app is created and configured
jwt = JWTManager(app)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models and routes to register them
import models
import routes
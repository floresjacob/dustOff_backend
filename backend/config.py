class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "your-secret-key"  # Change this to a secure key in production
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Set token expiration in seconds

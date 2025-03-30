from flask import Flask, request, jsonify
from models import db, User
import bcrypt
from app import app
from flask_cors import CORS

# Make sure the app instance has been created in your app.py and extensions initialized.
# If you haven't already imported the app from app.py here, you can either import it or create
# a blueprint for these routes.

CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return jsonify({'error': 'Missing fields'}), 400

    # Check if user already exists (optional)
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user
    new_user = User(username=username, password_hash=hashed_pw.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Login endpoint hit. Data received:", data)  # Debug print

    username = data.get('username')
    password = data.get('password')

    # Retrieve the user from the database
    user = User.query.filter_by(username=username).first()
    if user:
        print("User found:", user.username)
    else:
        print("No user found with username:", username)

    # Check password
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        print("Password check passed.")
        return jsonify({'message': 'Login successful'}), 200
    else:
        print("Invalid credentials provided.")
        return jsonify({'error': 'Invalid credentials'}), 401

# Optional: You might add more endpoints here for user management or protected content.
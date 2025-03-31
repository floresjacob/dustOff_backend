from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models import db, User
import bcrypt
from app import app


# Make sure the app instance has been created in your app.py and extensions initialized.
# If you haven't already imported the app from app.py here, you can either import it or create
# a blueprint for these routes.

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
        # Create JWT access token
        access_token = create_access_token(identity=username)
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        print("Invalid credentials provided.")
        return jsonify({'error': 'Invalid credentials'}), 401

# Optional: You might add more endpoints here for user management or protected content.
@app.route('/protected_hello', methods=['GET'])
@jwt_required()
def protected_hello():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}!'}), 200
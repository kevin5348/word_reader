#!/usr/bin/env python3
"""
Quick script to create a test user for development
"""
from app import create_app
from database.init_db import db, User
import bcrypt

def create_test_user():
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if test user already exists
        existing_user = User.query.filter_by(email='test@example.com').first()
        if existing_user:
            print("Test user already exists!")
            print(f"Email: test@example.com")
            print(f"Password: testpass")
            print(f"User ID: {existing_user.id}")
            print(f"Level: {existing_user.level}")
            return
        
        # Create test user
        hashed_password = bcrypt.hashpw('testpass'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        test_user = User(
            email='test@example.com',
            hashed_password=hashed_password,
            level=1.0  # Starting level
        )
        
        db.session.add(test_user)
        db.session.commit()
        
        print("✅ Test user created successfully!")
        print(f"Email: test@example.com")
        print(f"Password: testpass")
        print(f"User ID: {test_user.id}")
        print(f"Level: {test_user.level}")

if __name__ == "__main__":
    create_test_user()

#!/usr/bin/env python3
"""
Test script to verify the banking API setup is working correctly.
"""

import sys
import os
import sqlite3
from pathlib import Path

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        import alembic
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connection():
    """Test SQLite database connection."""
    print("Testing database connection...")
    try:
        # Test SQLite connection
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        print("✅ SQLite database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_app_structure():
    """Test that the app structure is correct."""
    print("Testing app structure...")
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "requirements.txt",
        "alembic.ini"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_fastapi_app():
    """Test that the FastAPI app can be created."""
    print("Testing FastAPI app creation...")
    try:
        from app.main import app
        print("✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Running Banking API Setup Tests\n")
    
    tests = [
        test_imports,
        test_database_connection,
        test_app_structure,
        test_fastapi_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The banking API setup is ready.")
        print("\nNext steps:")
        print("1. Copy env.example to .env and configure your settings")
        print("2. Run: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

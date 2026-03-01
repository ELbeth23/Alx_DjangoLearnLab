"""
Quick test script to verify API endpoints
Run with: python test_api.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test user registration endpoint"""
    url = f"{BASE_URL}/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "bio": "Test bio"
    }
    
    print("Testing Registration...")
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json().get('token')
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_login():
    """Test user login endpoint"""
    url = f"{BASE_URL}/login/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    print("\nTesting Login...")
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json().get('token')
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_profile(token):
    """Test profile endpoint with authentication"""
    url = f"{BASE_URL}/profile/"
    headers = {
        "Authorization": f"Token {token}"
    }
    
    print("\nTesting Profile...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Social Media API Test Suite")
    print("=" * 50)
    print("\nMake sure the server is running: python manage.py runserver\n")
    
    # Test registration
    token = test_registration()
    
    # Test login
    if not token:
        token = test_login()
    
    # Test profile
    if token:
        test_profile(token)
    
    print("\n" + "=" * 50)
    print("Tests completed!")
    print("=" * 50)

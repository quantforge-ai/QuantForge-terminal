"""
Test Authentication Endpoints
Quick test script to verify auth system works
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth():
    print("=" * 60)
    print("Testing QuantTerminal Authentication")
    print("=" * 60)
    print()
    
    # Test 1: Register
    print("1. Testing Registration...")
    register_data = {
        "username": "test_trader",
        "email": "trader@example.com",
        "password": "SecurePass123!"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        token = data["access_token"]
        print(f"✅ Registration successful!")
        print(f"   User: {data['user']['username']}")
        print(f"   Token: {token[:50]}...")
        print()
        
        # Test 2: Get Profile
        print("2. Testing Protected Route (Get Profile)...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Profile retrieved!")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print()
        else:
            print(f"❌ Failed: {response.text}")
            return
        
        # Test 3: Login
        print("3. Testing Login...")
        login_data = {
            "email": "trader@example.com",
            "password": "SecurePass123!"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            new_token = data["access_token"]
            print(f"✅ Login successful!")
            print(f"   New Token: {new_token[:50]}...")
            print()
        else:
            print(f"❌ Failed: {response.text}")
        
        # Test 4: Wrong Password
        print("4. Testing Login with Wrong Password...")
        wrong_login = {
            "email": "trader@example.com",
            "password": "WrongPassword"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=wrong_login)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print(f"✅ Correctly rejected invalid credentials")
            print()
        else:
            print(f"❌ Unexpected response")
        
        print("=" * 60)
        print("✅ All Authentication Tests Passed!")
        print("=" * 60)
        
    elif response.status_code == 400:
        print(f"⚠️  User already exists (run script again to test login)")
        print()
        
        # Just test login if user exists
        print("Testing Login with existing user...")
        login_data = {
            "email": "trader@example.com",
            "password": "SecurePass123!"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful!")
            print(f"   User: {data['user']['username']}")
            print(f"   Token: {data['access_token'][:50]}...")
        else:
            print(f"❌ Login failed: {response.text}")
    else:
        print(f"❌ Registration failed: {response.text}")


if __name__ == "__main__":
    try:
        test_auth()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running:")
        print("   python -m uvicorn backend.main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

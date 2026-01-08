import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
HEALTH_URL = f"{BASE_URL}/api/health"

TEST_EMAIL = "dev.burairahmed@gmail.com"
TEST_PASSWORD = "Burair1234"

def test_backend_health():
    try:
        print(f"Checking health at {HEALTH_URL}...")
        response = requests.get(HEALTH_URL, timeout=5)
        print(f"Health Status Code: {response.status_code}")
        print(f"Health Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_login():
    try:
        print(f"\nAttempting login at {LOGIN_URL}...")
        payload = {
            "email": TEST_EMAIL, 
            "password": TEST_PASSWORD
        }
        # API requires JSON
        response = requests.post(LOGIN_URL, json=payload, timeout=10)
        
        print(f"Login Status Code: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            print("Login Successful!")
        else:
            print("Login Failed.")
            
    except Exception as e:
        print(f"Login request failed: {e}")

def test_register():
    try:
        import uuid
        random_email = f"test_{uuid.uuid4()}@example.com"
        # Register endpoint expects UserCreate: name, email, password
        payload = {
            "name": "Test User",
            "email": random_email,
            "password": "TestPassword123"
        }
        print(f"\nAttempting register at {BASE_URL}/api/auth/register with {random_email}...")
        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload, timeout=10)
        
        print(f"Register Status Code: {response.status_code}")
        print(f"Register Response: {response.text}")
        
    except Exception as e:
        print(f"Register request failed: {e}")

if __name__ == "__main__":
    if test_backend_health():
        test_login()
        test_register()
    else:
        print("Skipping tests due to health check failure.")

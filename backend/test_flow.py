import requests

BASE_URL = "http://localhost:8000"

def test_flow():
    print("1. Registering new user...")
    register_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    register_response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print("Registration Response:", register_response.status_code)
    
    if register_response.status_code == 200:
        print("Registration successful:", register_response.json())
    else:
        print("Registration failed (user might exist):", register_response.text)

    print("\n2. Logging in...")
    login_data = {
        "username": "testuser@example.com",
        "password": "testpassword123"
    }
    login_response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    print("Login Response:", login_response.status_code)
    
    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        print("Login successful! Token received.")
    else:
        print("Login failed:", login_response.text)
        return

    print("\n3. Testing Scholarship DB Connection via API...")
    search_data = {
        "query": "merit",
        "language": "en"
    }
    search_response = requests.post(f"{BASE_URL}/api/scholarship/search", json=search_data)
    print("Search Response:", search_response.status_code)
    if search_response.status_code == 200:
        results = search_response.json()
        print(f"Search successful! Found {results.get('total_found')} scholarships matched.")
    else:
        print("Search failed:", search_response.text)

if __name__ == "__main__":
    test_flow()

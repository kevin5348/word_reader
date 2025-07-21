import requests
import json

# Test the API with some sample words
BASE_URL = "http://localhost:5000"

# First, let's test login to get a token
def test_api():
    # Test login with correct format (email instead of username)
    login_data = {
        "email": "test@example.com",
        "password": "testpass"
    }
    
    try:
        # Login
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("token")  # Changed from access_token
            print(f"Login successful, got token: {token[:20]}...")
            
            # Test get_difficulties
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Test with some simple words
            test_words = "hello,world,difficult,complex,simple"
            
            response = requests.get(
                f"{BASE_URL}/get_difficulties?words={test_words}",
                headers=headers
            )
            
            print(f"API Response Status: {response.status_code}")
            print(f"API Response: {response.text}")
            
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_api()
    test_api()

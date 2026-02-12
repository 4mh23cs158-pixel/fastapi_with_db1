import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"

def run_verification():
    # 1. Signup
    email = f"test_user_{uuid.uuid4()}@example.com"
    password = "password123"
    print(f"Testing with email: {email}")
    
    signup_payload = {"name": "Test User", "email": email, "password": password}
    try:
        res = requests.post(f"{BASE_URL}/signup", json=signup_payload)
        print(f"Signup Status: {res.status_code}")
        if res.status_code != 200:
            print(f"Signup Failed: {res.text}")
            return
    except Exception as e:
        print(f"Signup Exception: {e}")
        return

    # 2. Login
    login_payload = {"email": email, "password": password}
    try:
        res = requests.post(f"{BASE_URL}/login", json=login_payload)
        print(f"Login Status: {res.status_code}")
        if res.status_code != 200:
            print(f"Login Failed: {res.text}")
            return
        tokens = res.json()
        access_token = tokens.get("access_token")
        if not access_token:
            print("No access token returned")
            return
        print("Login Successful, Token Received")
    except Exception as e:
        print(f"Login Exception: {e}")
        return

    # 3. Ask AI (Create Chat)
    headers = {"Authorization": f"Bearer {access_token}"}
    ask_payload = {
        "message": "Hello, this is a test message.",
        "system_prompt": "You are a helpful assistant."
    }
    try:
        res = requests.post(f"{BASE_URL}/ask", json=ask_payload, headers=headers)
        print(f"Ask AI Status: {res.status_code}")
        if res.status_code != 200:
            print(f"Ask AI Failed: {res.text}")
            return
        ai_data = res.json()
        session_id = ai_data.get("session_id")
        print(f"AI Response: {ai_data.get('response')}")
        print(f"Session ID: {session_id}")
    except Exception as e:
        print(f"Ask AI Exception: {e}")
        return

    # 4. Get History
    try:
        res = requests.get(f"{BASE_URL}/history/{session_id}", headers=headers)
        print(f"History Status: {res.status_code}")
        if res.status_code != 200:
            print(f"History Failed: {res.text}")
            return
        history = res.json().get("history", [])
        print(f"History Retrieved: {len(history)} messages")
        if len(history) >= 2:
            print("Verification PASSED: User and Chat History saved successfully.")
        else:
            print("Verification WARNING: History count mismatch.")
    except Exception as e:
        print(f"History Exception: {e}")
        return

if __name__ == "__main__":
    run_verification()

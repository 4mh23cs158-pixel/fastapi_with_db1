import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_sessions():
    email = "persist_test@example.com"
    password = "securepass123"
    
    print(f"Logging in as {email}...")
    try:
        # Login
        resp = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
        if resp.status_code != 200:
            print(f"Login Failed: {resp.text}")
            return
        token = resp.json()["access_token"]
        
        # Get Sessions
        print("Fetching sessions...")
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/sessions", headers=headers)
        
        if resp.status_code == 200:
            sessions = resp.json().get("sessions", [])
            print(f"SUCCESS: Retrieved {len(sessions)} sessions.")
            for s in sessions:
                print(f" - ID: {s['session_id']}, Title: {s['title']}, Time: {s['last_message_at']}")
        else:
            print(f"FAILURE: Sessions endpoint returned {resp.status_code}: {resp.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_sessions()

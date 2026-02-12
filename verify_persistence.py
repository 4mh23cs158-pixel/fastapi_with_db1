import requests
import sys
from sqlalchemy import create_engine, text
from db import DATABASE_URL

# API URL
BASE_URL = "http://127.0.0.1:8000"

def check_db_counts():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        user_count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
        chat_count = conn.execute(text("SELECT COUNT(*) FROM chat_messages")).scalar()
        print(f"DATABASE CHECK: Users: {user_count}, Chat Messages: {chat_count}")
    return user_count, chat_count

def test_signup(email, password):
    print(f"Testing Signup for {email}...")
    try:
        response = requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})
        if response.status_code == 200:
            print("Signup API: Success")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
             print("Signup API: User already exists (Expected)")
             return True
        else:
            print(f"Signup API Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Signup API Connection Error: {e}")
        return False

def test_login(email, password):
    print(f"Testing Login for {email}...")
    try:
        response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("Login API: Success, Token obtained")
            return token
        else:
            print(f"Login API Failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Login API Connection Error: {e}")
        return None

def test_chat(token, message):
    print(f"Testing Chat with message: '{message}'...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/ask", json={"message": message}, headers=headers)
        if response.status_code == 200:
            print("Chat API: Success")
            return response.json().get("session_id")
        else:
            print(f"Chat API Failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Chat API Connection Error: {e}")
        return None

def main():
    print("--- STARTING PERSISTENCE CHECK ---")
    
    # Check initial counts
    try:
        initial_users, initial_chats = check_db_counts()
    except Exception as e:
        print(f"CRITICAL: Cannot connect to database directly: {e}")
        return

    # Test User Flow
    test_email = "persist_test@example.com"
    test_pass = "securepass123"
    
    if test_signup(test_email, test_pass):
        token = test_login(test_email, test_pass)
        if token:
            # Test Chat Flow
            test_chat(token, "Persistence Test Message")
            
            # Check counts again
            print("\n--- VERIFYING CHANGES ---")
            final_users, final_chats = check_db_counts()
            
            if final_users > initial_users: # Note: might be equal if user already existed
                print("SUCCESS: User count increased.")
            else:
                 print(f"INFO: User count unchanged (User might verify manually: {initial_users} -> {final_users})")

            if final_chats > initial_chats:
                print("SUCCESS: Chat message count increased.")
            else:
                print("FAILURE: Chat message count did NOT increase.")
        else:
            print("FAILURE: Could not log in to test chat.")
    else:
        print("FAILURE: Signup failed.")

if __name__ == "__main__":
    main()

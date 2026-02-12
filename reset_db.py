from db import engine, Base
from models import ChatMessage
from sqlalchemy import text

def reset_chat_table():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS chat_messages CASCADE"))
        conn.execute(text("COMMIT"))
    print("Dropped chat_messages table.")
    
    # Recreate tables
    Base.metadata.create_all(engine)
    print("Recreated tables.")

if __name__ == "__main__":
    reset_chat_table()

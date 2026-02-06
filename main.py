from fastapi import FastAPI
from routes.user_routes import router as user_router
from sqlalchemy import create_engine
import os
from db import DATABASE_URL
from models import Base
app = FastAPI() 

app.include_router(user_router)
# to create database
if not os.path.exists("./test.db"):
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000, reload=True)

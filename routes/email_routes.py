from fastapi import APIRouter ,Depends
from sqlalchemy.orm import Session
from db import get_db
from utils.email_sender import send_email

router = APIRouter()

@router.post("/send-email")
def send_email_route(email: str, subject: str, content: str, db: Session = Depends(get_db)):
   """
   send an email to the reciever with the given subject and content
   
   """
   
   send_email(email, subject, content)
   return {"message": "Email sent successfully!"}

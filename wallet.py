from fastapi import APIRouter, Request
from models import db_users

router = APIRouter()

@router.post("/create-order")
def create_order(request: Request):
    # Dummy Razorpay order creation simulation
    return {"id": "order_Dummy123", "amount": 10000, "currency": "INR"}

@router.post("/verify-payment")
def verify_payment(request: Request):
    data = await request.json()
    username = data.get("username")
    db_users[username]["balance"] += int(data.get("amount", 0))
    return {"status": "success"}

@router.get("/balance")
def get_balance(username: str):
    return {"balance": db_users[username]["balance"]}

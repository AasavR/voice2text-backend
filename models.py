from typing import Dict

db_users: Dict[str, dict] = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "balance": 0
    }
}

class User:
    def __init__(self, username: str, password: str, balance: int = 0):
        self.username = username
        self.password = password
        self.balance = balance

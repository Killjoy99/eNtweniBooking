from typing import List, Optional
from fastapi import Request


class LoginForm():
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: str
        self.password: str
        self.remember_me: str
        
    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        self.remember_me = form.get("remember_me")
        
    def is_valid(self):
        if not self.username or not len(self.username) >= 4:
            self.errors.append("A valid username is required")
        if not self.password or not len(self.username) >= 8:
            self.errors.append("A valid password is required")
            
        if not self.errors:
            return True
        return False
    
class RegisterForm():
    pass


class ResetPassword():
    pass
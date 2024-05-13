

class AuthenticationService():
    def __init__(self):
        pass

    def login(self, remember_me: bool = False, username: str = None, password: str = None):
        # check user from the database
        if username != "admin" or password != "admin123":
            return False
        else:
            return True
        
    def logout(self, token: str):
        # expire the token and redirect the user to  the login screen
        pass
    
    # other methods to generate JWT for auth and revoke them, ban users, blacklist users etc.
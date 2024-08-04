import hashlib

class AuthService:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(stored_password, provided_password):
        return stored_password == AuthService.hash_password(provided_password)

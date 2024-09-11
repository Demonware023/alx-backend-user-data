from db import DB
from user import User
import bcrypt

class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user."""
        try:
            user = self._db.add_user(email, self._hash_password(password))
            return user
        except ValueError as e:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        # Check if the hashed password matches
        return bcrypt.checkpw(password.encode(), user.hashed_password.encode())

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

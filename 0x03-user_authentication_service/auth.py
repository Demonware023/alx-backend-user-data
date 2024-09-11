from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from auth import _hash_password

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the provided email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If the user with the given email already exists.
        """
        try:
            # Check if the user already exists by email
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If user doesn't exist, proceed to create the new user
            hashed_password = _hash_password(password)  # Hash the password
            new_user = self._db.add_user(email, hashed_password)  # Add user to the DB
            return new_user  # Return the newly created user

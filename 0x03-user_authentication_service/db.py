#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class for interacting with the database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database and returns the User object"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by arbitrary keyword arguments.

        Args:
            kwargs: Arbitrary keyword arguments to filter the users table.

        Returns:
            User: The user that matches the provided filters.

        Raises:
            NoResultFound: If no user matches the filter.
            InvalidRequestError: If an invalid column is provided.
        """
        try:
            # Try to find the user using filter_by
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound()

            return user

        except InvalidRequestError:
            # This will catch errors like invalid column names
            raise InvalidRequestError()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes and commits the changes to the database.

        Args:
            user_id (int): The ID of the user to update.
            kwargs: Arbitrary keyword arguments to update user attributes.

        Raises:
            ValueError: If a keyword argument does not match any User attribute.
        """
        try:
            # Find the user using the provided user_id
            user = self.find_user_by(id=user_id)

            # Iterate over the keyword arguments and update the user attributes
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"{key} is not a valid attribute of User")

                setattr(user, key, value)

            # Commit the changes to the database
            self._session.commit()

        except NoResultFound:
            raise ValueError(f"User with id {user_id} not found")

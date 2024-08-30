#!/usr/bin/env python3
"""
Module for password hashing
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the salted,
    hashed password as a byte string.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

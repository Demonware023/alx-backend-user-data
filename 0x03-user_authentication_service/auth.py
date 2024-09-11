#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.hashpw with a salt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt() # Generate a salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt) # Hash the password
    return hashed

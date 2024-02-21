#!/usr/bin/env python3
"""module for authentication"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with salt"""

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new instance of DB"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f"User {email} already exists")
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login credentials are valid"""

        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)

            # If user exists, check if the password matches
            stored_password = user.hashed_password
            entered_password = password.encode('utf-8')
            return bcrypt.checkpw(entered_password, stored_password)
        except NoResultFound:
            # If user does not exist, return False
            return False

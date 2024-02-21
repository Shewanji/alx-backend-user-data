#!/usr/bin/env python3
"""module for authentication"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union

def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with salt"""

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation"""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """Create a session for the user and return the session ID"""
        try:
            # Find the user corresponding to the email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        # Generate a new UUID for the session ID
        session_id = _generate_uuid()

        # Update the user's session_id in the database
        self._db.update_user(user.id, session_id=session_id)

        # Return the session ID
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user corresponding to the given session ID"""

        # If session_id is None, return None
        if session_id is None:
            return None

        try:
            # Find user by session_id using the DB's find_user_by method
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            # If no user is found, return None
            return None

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

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the corresponding user"""

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate and return a reset password token for the user"""

        try:
            # Find the user corresponding to the email
            user = self._db.find_user_by(email=email)

            # Generate a UUID for the reset token
            reset_token = str(uuid.uuid4())

            # Update the user's reset_token in the database
            self._db.update_user(user.id, reset_token=reset_token)

            # Return the reset token
            return reset_token

        except NoResultFound:
            # If user does not exist, raise a ValueError exception
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password using reset token"""

        try:
            # Find the corresponding user using the reset_token
            user = self._db.find_user_by(reset_token=reset_token)

            # Update the user's hashed_password and reset_token in database
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)

        except NoResultFound:
            # If user does not exist, raise a ValueError exception
            raise ValueError()

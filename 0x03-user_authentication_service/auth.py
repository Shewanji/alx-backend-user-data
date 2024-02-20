#!/usr/bin/env python3
"""module for authentication"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with salt"""

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

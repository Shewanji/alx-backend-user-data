#!/usr/bin/env python3
"""module for the clas auth"""

from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if authentication is required for a given path."""

        return False

    def authorization_header(self, request=None) -> str:
        """ Retrieve the Authorization header from the request."""

        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Retrieves the current user based on the provided request."""

        return None
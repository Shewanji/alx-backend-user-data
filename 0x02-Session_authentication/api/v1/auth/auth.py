#!/usr/bin/env python3

"""module for the clas auth"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if authentication is required for a given path."""

        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'
        return not (path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """ Retrieve the Authorization header from the request."""

        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Retrieves the current user based on the provided request."""

        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request."""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True

#!/usr/bin/env python3
"""module for BasicAuth class"""

import base64

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """class for BasicAuth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header
        for Basic Authentication."""

        if authorization_header is None or not isinstance(
                authorization_header, str):

            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

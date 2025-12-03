"""
api_auth.py

Token-based authentication helper.
Manages login and token validation for protected endpoints.
"""

import uuid
from django.http import JsonResponse
from api_data import VALID_TOKENS


def check_authentication(request):
    """
    Verify Authorization header contains valid token.
    
    Returns: (is_authenticated: bool, username_or_none, error_response_or_none)
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    token = auth_header.replace('Bearer ', '').strip()
    
    if not token:
        return False, None, JsonResponse({
            'success': False,
            'message': 'Missing Authorization header. Use: Authorization: Bearer <token>'
        }, status=401)
    
    username = VALID_TOKENS.get(token)
    if not username:
        return False, None, JsonResponse({
            'success': False,
            'message': 'Invalid or expired token. Please login via /api/auth/login/'
        }, status=401)
    
    return True, username, None


def create_token(username):
    """
    Create and store a new authentication token.
    Returns the token string.
    """
    token = str(uuid.uuid4())
    VALID_TOKENS[token] = username
    return token


def validate_login_format(username, password):
    """
    Validate username and password format.
    
    Current rules:
    - Username: 4 letters
    - Password: 2 letters + 2 digits (e.g., "ab12")
    
    CUSTOMIZE THIS for your app!
    Replace with Django User auth or your own rules.
    """
    errors = []
    
    if not (len(username) == 4 and username.isalpha()):
        errors.append('Username must be 4 letters')
    
    if not (len(password) == 4 and password[:2].isalpha() and password[2:].isdigit()):
        errors.append('Password must be 2 letters + 2 numbers (e.g., ab12)')
    
    return errors

from typing import Dict, Union
from flask_jwt_extended import create_access_token
from App.models import User
from .base_controller import BaseController

class AuthController(BaseController):
    """Controller for authentication operations"""

    @classmethod
    def login(cls, username: str, password: str) -> Union[str, None]:
        """Authenticate a user and return a JWT token"""
        try:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                return create_access_token(identity=user.id)
            return None
        except Exception as e:
            return None

    @classmethod
    def verify_token(cls, token: str) -> Union[User, None]:
        """Verify a JWT token and return the user"""
        try:
            # This is just a placeholder - actual implementation would use JWT decode
            return None
        except Exception:
            return None

    @classmethod
    def get_current_user(cls) -> Union[Dict, None]:
        """Get the current authenticated user's details"""
        try:
            from flask_jwt_extended import current_user
            if current_user:
                return cls.to_json(current_user)
            return None
        except Exception:
            return None
from flask import jsonify
from typing import Dict, Any, Union

class BaseController:
    """Base controller class with common utility methods"""
    
    @staticmethod
    def success_response(data: Any = None, message: str = "Success") -> Dict:
        """Standard success response format"""
        response = {
            "success": True,
            "message": message
        }
        if data is not None:
            response["data"] = data
        return response

    @staticmethod
    def error_response(message: str, code: int = 400) -> Dict:
        """Standard error response format"""
        return {
            "success": False,
            "message": message,
            "error_code": code
        }

    @staticmethod
    def to_json(data: Any) -> Dict:
        """Convert model instances to JSON"""
        if hasattr(data, '__dict__'):
            return {k: v for k, v in data.__dict__.items() if not k.startswith('_')}
        return data
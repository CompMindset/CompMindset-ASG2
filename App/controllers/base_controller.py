from typing import Any, Dict, Union
from flask import jsonify
from datetime import datetime

class BaseController:
    """Base controller class with common utility methods"""
    
    @staticmethod
    def success_response(data: Any = None, message: str = "Success") -> Dict:
        """Standard success response format"""
        response = {
            "success": True,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
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
            "error_code": code,
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def to_json(data: Any) -> Dict:
        """Convert model instances to JSON"""
        if hasattr(data, 'get_json'):
            return data.get_json()
        elif hasattr(data, '__dict__'):
            return {k: v for k, v in data.__dict__.items() if not k.startswith('_')}
        return data
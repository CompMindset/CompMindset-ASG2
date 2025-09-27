from typing import Union, List
from App.database import db
from App.models import Admin, Staff, User

def create_user(role: str, full_name: str, email: str, username: str, password: str):
    r = role.upper()
    if r == "ADMIN":
        u = Admin(full_name=full_name, email=email, username=username, password=password)
    elif r == "STAFF":
        u = Staff(full_name=full_name, email=email, username=username, password=password)
    else:
        raise ValueError("Role must be ADMIN or STAFF")
    db.session.add(u)
    db.session.commit()
    return u

def get_user_by_username(username: str) -> Union[User, None]:
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def list_users() -> List[User]:
    return db.session.execute(db.select(User)).scalars().all()

def get_all_users():
    """Alias for list_users for compatibility with views"""
    return list_users()

def get_all_users_json():
    """Returns all users as JSON-serializable data"""
    users = list_users()
    return [{'id': u.id, 'username': u.username, 'full_name': u.full_name, 'email': u.email, 'role': u.role} for u in users]

def get_user(user_id: int) -> Union[User, None]:
    """Get user by ID"""
    result = db.session.execute(db.select(User).filter_by(id=user_id))
    return result.scalar_one_or_none()

def update_user(user_id: int, **kwargs) -> Union[User, None]:
    """Update user with given fields"""
    user = get_user(user_id)
    if not user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.session.commit()
    return user

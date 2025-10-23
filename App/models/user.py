from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "ADMIN" | "STAFF"

    # joined-table inheritance
    type = db.Column(db.String(50))
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "user"}

    def __init__(self, full_name, email, username, password, role):
        self.full_name = full_name
        self.email = email
        self.username = username
        self.set_password(password)
        self.role = role.upper()

    # screenshot-style helpers
    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
        }

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # keep simple diagram methods (no-op)
    def login(self, id: int, password_hash: str):
        return self.id == id and self.password_hash == password_hash

    def logout(self):
        return True

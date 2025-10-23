from App.database import db
from .user import User

class Admin(User):
    __tablename__ = "admins"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "admin"}

    # optional explicit pass-through constructor
    def __init__(self, full_name, email, username, password, role="ADMIN"):
        super().__init__(full_name, email, username, password, role)

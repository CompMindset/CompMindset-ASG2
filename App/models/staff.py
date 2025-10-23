from App.database import db
from .user import User

class Staff(User):
    __tablename__ = "staff"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "staff"}

    def __init__(self, full_name, email, username, password, role="STAFF"):
        super().__init__(full_name, email, username, password, role)


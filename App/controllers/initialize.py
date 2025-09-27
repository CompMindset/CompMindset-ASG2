from .user import create_user
from App.database import db

def initialize():
    """
    Reset the database and seed a minimal dataset.

    Mirrors the simple pattern:
      db.drop_all()
      db.create_all()
      create_user(...)
    """
    db.drop_all()
    db.create_all()

    # Seed users (passwords hashed by the model constructor)
    admin  = create_user('ADMIN', 'Alice Admin', 'alice@x.com', 'admin1', 'adminpass')
    staff1 = create_user('STAFF', 'Sam Staff',   'sam@x.com',   'staff1', 'staffpass')
    staff2 = create_user('STAFF', 'Pat Worker',  'pat@x.com',   'staff2', 'staffpass')

    return f"Initialized. Admin id={admin.id}; Staff ids={[staff1.id, staff2.id]}"

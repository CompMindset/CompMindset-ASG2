from datetime import datetime, date
from App.database import db
from App.models import Shift, Admin, Staff

def create_shift(admin_id:int, start_iso:str, end_iso:str, location:str, week_start_iso:str):
    admin = Admin.query.get(admin_id)
    if not admin:
        raise ValueError("Admin not found")
    s = Shift(
        admin_id=admin.id,
        start_time=datetime.fromisoformat(start_iso),
        end_time=datetime.fromisoformat(end_iso),
        location=location,
        week_start=date.fromisoformat(week_start_iso),
        status="OPEN"
    )
    db.session.add(s)
    db.session.commit()
    return s

def assign_shift(shift_id:int, staff_id:int):
    s = Shift.query.get(shift_id)
    st = Staff.query.get(staff_id)
    if not s or not st:
        raise ValueError("Shift/Staff not found")
    s.assignTo(st.id)
    db.session.commit()
    return s

def publish_roster(week_start_iso:str):
    w = date.fromisoformat(week_start_iso)
    return Shift.query.filter_by(week_start=w).order_by(Shift.start_time).all()

def list_all_shifts():
    return Shift.query.order_by(Shift.start_time).all()

from datetime import datetime
from App.database import db
from App.models import Attendance, Shift, Staff

LATE_GRACE_SECONDS = 300  # 5 minutes

def clock_in(shift_id:int, staff_id:int, ts_iso:str):
    shift = Shift.query.get(shift_id)
    staff = Staff.query.get(staff_id)
    if not shift or not staff:
        raise ValueError("Shift/Staff not found")
    rec = Attendance.query.filter_by(shift_id=shift_id, staff_id=staff_id).first()
    if not rec:
        rec = Attendance(shift_id=shift_id, staff_id=staff_id)
        db.session.add(rec)
    t = datetime.fromisoformat(ts_iso)
    rec.clockIn = t
    rec.status = "ON_TIME" if (t - shift.start_time).total_seconds() <= LATE_GRACE_SECONDS else "LATE"
    db.session.commit()
    return rec

def clock_out(shift_id:int, staff_id:int, ts_iso:str):
    rec = Attendance.query.filter_by(shift_id=shift_id, staff_id=staff_id).first()
    if not rec:
        raise ValueError("Clock-in record not found")
    rec.clockOut = datetime.fromisoformat(ts_iso)
    db.session.commit()
    return rec

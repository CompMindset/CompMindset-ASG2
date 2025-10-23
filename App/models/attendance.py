from App.database import db
from sqlalchemy import CheckConstraint

class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)   # attendanceID
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"),  nullable=False)
    clockIn  = db.Column(db.DateTime, nullable=True)
    clockOut = db.Column(db.DateTime, nullable=True)
    status   = db.Column(db.String(10), nullable=True)  # ON_TIME|LATE|EARLY|MISSED

    shift = db.relationship("Shift", backref="attendance_records", lazy=True)

    __table_args__ = (
        CheckConstraint("status in ('ON_TIME','LATE','EARLY','MISSED') or status is null",
                        name="attendance_status_chk"),
    )

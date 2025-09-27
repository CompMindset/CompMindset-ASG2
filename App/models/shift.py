from App.database import db

class Shift(db.Model):
    __tablename__ = "shifts"
    id = db.Column(db.Integer, primary_key=True)           # shiftID
    staff_id  = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=True)
    admin_id  = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    location   = db.Column(db.String(120), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time   = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(12), nullable=False, default="OPEN")  # OPEN|ASSIGNED|COMPLETED

    staff = db.relationship("Staff", backref="shifts", lazy=True)
    admin = db.relationship("Admin", backref="created_shifts", lazy=True)

    def assignTo(self, staffID: int):
        self.staff_id = staffID
        self.status = "ASSIGNED"

    def reschedule(self, start, end):
        self.start_time = start
        self.end_time = end

    def duration(self):
        return (self.end_time - self.start_time).total_seconds() / 3600.0

    def markDone(self):
        self.status = "COMPLETED"


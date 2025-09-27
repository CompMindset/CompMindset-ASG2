from App.database import db
from sqlalchemy import CheckConstraint
from datetime import datetime

class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)  # requestID
    requestingStaffID = db.Column(db.Integer, db.ForeignKey("staff.id"),  nullable=False)
    assignedAdminID   = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    type  = db.Column(db.String(10), nullable=False)  # SWAP | TIME-OFF
    status = db.Column(db.String(10), nullable=False, default="PENDING")  # PENDING|APPROVED|REJECTED|CANCELLED
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    decidedAt = db.Column(db.DateTime, nullable=True)
    reason    = db.Column(db.String(255), nullable=True)
    target_shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("\"type\" in ('SWAP','TIME-OFF')", name="request_type_chk"),
        CheckConstraint("status in ('PENDING','APPROVED','REJECTED','CANCELLED')", name="request_status_chk"),
    )

    def cancel(self):
        self.status = "CANCELLED"
        self.decidedAt = datetime.utcnow()

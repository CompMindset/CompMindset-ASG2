from App.database import db
from datetime import datetime

class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)  # reportID
    weekStart   = db.Column(db.Date, nullable=False)
    generatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    totalShifts = db.Column(db.Integer, nullable=False, default=0)
    totalHours  = db.Column(db.Numeric(10,2), nullable=False, default=0)

    def generateRoster(self):
        return True

    def generateReport(self):
        return True

from decimal import Decimal
from datetime import date
from App.database import db
from App.models import Report, Shift

def generate_weekly_report(week_start_iso:str):
    w = date.fromisoformat(week_start_iso)
    shifts = Shift.query.filter_by(week_start=w).all()
    hours = sum([s.duration() for s in shifts]) if shifts else 0
    rpt = Report(weekStart=w, totalShifts=len(shifts), totalHours=Decimal(hours))
    db.session.add(rpt)
    db.session.commit()
    return rpt

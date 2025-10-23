from typing import List, Dict, Union
from datetime import datetime
from App.database import db
from App.models import Shift
from .base_controller import BaseController

class ShiftController(BaseController):
    """Controller for shift management operations"""

    @classmethod
    def create_shift(cls, admin_id: int, start_iso: str, end_iso: str, location: str, week_start_iso: str) -> Union[Shift, None]:
        """Create a new shift"""
        try:
            start_time = datetime.fromisoformat(start_iso)
            end_time = datetime.fromisoformat(end_iso)
            week_start = datetime.fromisoformat(week_start_iso)
            
            shift = Shift(
                admin_id=admin_id,
                start_time=start_time,
                end_time=end_time,
                location=location,
                week_start=week_start,
                status="OPEN"
            )
            
            db.session.add(shift)
            db.session.commit()
            return shift
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def assign_shift(cls, shift_id: int, staff_id: int) -> Union[Shift, None]:
        """Assign a shift to a staff member"""
        try:
            shift = Shift.query.get(shift_id)
            if not shift:
                raise ValueError(f"Shift {shift_id} not found")
            
            shift.staff_id = staff_id
            shift.status = "ASSIGNED"
            db.session.commit()
            return shift
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def publish_roster(cls, week_start_iso: str) -> List[Shift]:
        """Get and publish all shifts for a given week"""
        week_start = datetime.fromisoformat(week_start_iso)
        shifts = Shift.query.filter_by(week_start=week_start).all()
        return shifts

    @classmethod
    def list_all_shifts(cls) -> List[Shift]:
        """Get all shifts in the system"""
        return Shift.query.all()

    @classmethod
    def get_shift(cls, shift_id: int) -> Union[Shift, None]:
        """Get a shift by ID"""
        return Shift.query.get(shift_id)

    @classmethod
    def get_shifts_for_staff(cls, staff_id: int) -> List[Shift]:
        """Get all shifts assigned to a staff member"""
        return Shift.query.filter_by(staff_id=staff_id).all()

    @classmethod
    def get_shifts_for_week(cls, week_start_iso: str) -> List[Shift]:
        """Get all shifts for a specific week"""
        week_start = datetime.fromisoformat(week_start_iso)
        return Shift.query.filter_by(week_start=week_start).all()

    @classmethod
    def update_shift_status(cls, shift_id: int, new_status: str) -> Union[Shift, None]:
        """Update a shift's status"""
        try:
            shift = cls.get_shift(shift_id)
            if not shift:
                return None
            
            shift.status = new_status
            db.session.commit()
            return shift
        except Exception as e:
            db.session.rollback()
            raise e
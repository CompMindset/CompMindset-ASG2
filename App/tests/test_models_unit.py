import pytest
from datetime import datetime, timedelta, date

from App.models import Shift, Request


pytestmark = pytest.mark.unit


def test_shift_duration_assign_and_complete():
    start = datetime.utcnow().replace(microsecond=0)
    end = start + timedelta(hours=3.5)
    s = Shift(admin_id=1, week_start=date.today(), location='HQ', start_time=start, end_time=end)

    # duration
    assert round(s.duration(), 2) == 3.5

    # assign
    s.assignTo(42)
    assert s.staff_id == 42 and s.status == 'ASSIGNED'

    # reschedule and duration change
    new_end = start + timedelta(hours=2)
    s.reschedule(start, new_end)
    assert round(s.duration(), 2) == 2.0

    # complete
    s.markDone()
    assert s.status == 'COMPLETED'


def test_request_cancel_sets_status_and_time():
    r = Request(requestingStaffID=10, assignedAdminID=1, type='SWAP', reason='need time', target_shift_id=None)
    # SQLAlchemy column defaults are applied on insert; prior to DB flush, status may be None
    assert r.status in (None, 'PENDING')
    r.cancel()
    assert r.status == 'CANCELLED'
    assert r.decidedAt is not None

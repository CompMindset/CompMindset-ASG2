import pytest
from datetime import datetime, timedelta

from App.main import create_app
from App.database import db, create_db
from App.controllers import (
    create_user,
    create_shift,
    assign_shift,
    clock_in,
    clock_out,
    publish_roster,
    list_all_shifts,
    generate_weekly_report,
    make_request,
    decide_request,
)


pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def setup_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_ctrl.db'})
    create_db()
    yield app
    db.drop_all()


def test_attendance_and_roster_flow(setup_db):
    from datetime import date

    # seed users
    admin = create_user('ADMIN', 'A Admin', 'a@x.com', 'adminA', 'pass')
    staff = create_user('STAFF', 'S Staff', 's@x.com', 'staffS', 'pass')

    # create a shift
    start = datetime.utcnow().replace(microsecond=0)
    end = start + timedelta(hours=2)
    week = start.date().isoformat()
    shift = create_shift(admin.id, start.isoformat(), end.isoformat(), 'Lab', week)

    # assign
    shift = assign_shift(shift.id, staff.id)
    assert shift.status == 'ASSIGNED' and shift.staff_id == staff.id

    # clock in/out
    rec = clock_in(shift.id, staff.id, start.isoformat())
    assert rec.status in ('ON_TIME', 'LATE') and rec.clockIn is not None
    rec = clock_out(shift.id, staff.id, end.isoformat())
    assert rec.clockOut is not None

    # list/publish
    all_shifts = list_all_shifts()
    assert any(s.id == shift.id for s in all_shifts)
    roster = publish_roster(week)
    assert any(s.id == shift.id for s in roster)

    # weekly report
    rpt = generate_weekly_report(week)
    assert rpt.totalShifts >= 1


def test_requests_flow(setup_db):
    # create users and a shift to reference
    admin = create_user('ADMIN', 'B Admin', 'b@x.com', 'adminB', 'pass')
    staff = create_user('STAFF', 'T Staff', 't@x.com', 'staffT', 'pass')
    start = datetime.utcnow().replace(microsecond=0)
    end = start + timedelta(hours=1)
    week = start.date().isoformat()
    shift = create_shift(admin.id, start.isoformat(), end.isoformat(), 'HQ', week)

    # make and decide request
    req = make_request(staff.id, admin.id, 'SWAP', reason='conflict', shift_id=shift.id)
    assert req.type == 'SWAP' and req.status == 'PENDING'
    decided = decide_request(req.id, 'APPROVED')
    assert decided.status == 'APPROVED' and decided.decidedAt is not None

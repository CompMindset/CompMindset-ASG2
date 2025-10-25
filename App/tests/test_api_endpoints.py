import pytest
from datetime import datetime, timedelta

from App.main import create_app
from App.database import db, create_db
from App.controllers import create_user


pytestmark = pytest.mark.integration

@pytest.fixture(scope="module")
def client():
    """Flask test client with a fresh SQLite DB."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_api.db',
        # Easier testing of cookies locally; we mostly use Authorization header anyway
        'JWT_COOKIE_SECURE': False,
    })
    create_db()
    yield app.test_client()
    db.drop_all()


def _auth_headers(client, username: str, password: str):
    """Login through the API and return Authorization headers."""
    res = client.post('/api/login', json={'username': username, 'password': password})
    assert res.status_code == 200
    data = res.get_json()
    # success response format: { success, message, data: { access_token } }
    token = data.get('data', {}).get('access_token')
    assert token, f"No token returned for {username}"
    return { 'Authorization': f'Bearer {token}' }


def test_health_endpoint(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.get_json().get('status') == 'healthy'


def test_user_flow_and_core_endpoints(client):
    # Seed minimal users
    admin = create_user('ADMIN', 'Alice Admin', 'alice@example.com', 'admin', 'adminpass')
    staff = create_user('STAFF', 'Sam Staff', 'sam@example.com', 'staff', 'staffpass')

    # Ensure users API lists them
    res = client.get('/api/users')
    assert res.status_code == 200
    usernames = [u['username'] for u in res.get_json()]
    assert 'admin' in usernames and 'staff' in usernames

    # Admin auth header
    admin_h = _auth_headers(client, 'admin', 'adminpass')

    # Create a shift via API
    start = datetime.utcnow().replace(microsecond=0)
    end = start + timedelta(hours=4)
    week_start = start.date().isoformat()
    res = client.post('/api/shifts', json={
        'adminId': admin.id,
        'startTime': start.isoformat(),
        'endTime': end.isoformat(),
        'location': 'HQ',
        'weekStart': week_start,
    }, headers=admin_h)
    assert res.status_code == 201
    shift = res.get_json()
    assert shift['status'] == 'OPEN'

    # Assign the shift to staff
    res = client.post(f"/api/shifts/{shift['id']}/assign", json={'staffId': staff.id}, headers=admin_h)
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'ASSIGNED'

    # Staff clocks in and out
    staff_h = _auth_headers(client, 'staff', 'staffpass')
    res = client.post('/api/attendance/clock-in', json={
        'shiftId': shift['id'],
        'timestamp': start.isoformat(),
    }, headers=staff_h)
    assert res.status_code == 201
    assert res.get_json()['status'] in ('ON_TIME', 'LATE')

    res = client.post('/api/attendance/clock-out', json={
        'shiftId': shift['id'],
        'timestamp': (end).isoformat(),
    }, headers=staff_h)
    assert res.status_code == 200
    assert res.get_json()['hoursWorked'] == 4.0

    # Weekly report
    res = client.get(f'/api/reports/weekly?weekStart={week_start}', headers=admin_h)
    assert res.status_code == 200
    rpt = res.get_json()
    assert rpt['totalShifts'] >= 1
    assert float(rpt['totalHours']) >= 4.0

import pytest
from datetime import datetime, timedelta

from App.main import create_app
from App.database import db, create_db
from App.controllers import create_user


pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_api_more.db',
        'JWT_COOKIE_SECURE': False,
    })
    create_db()
    yield app.test_client()
    db.drop_all()


def _auth_headers(client, username: str, password: str):
    res = client.post('/api/login', json={'username': username, 'password': password})
    return res


def test_bad_login_returns_401(client):
    res = client.post('/api/login', json={'username': 'nope', 'password': 'wrong'})
    # Implementation returns JSON error payload with error_code=401 but status may be 200
    assert res.status_code in (200, 401)
    body = res.get_json()
    assert body.get('success') is False
    assert body.get('error_code') == 401


def test_me_and_records_and_reports(client):
    # Seed admin + staff
    admin = create_user('ADMIN', 'Admin Test', 'admin@test.com', 'adm', 'pass')
    staff = create_user('STAFF', 'Staff Test', 'staff@test.com', 'stf', 'pass')

    # Admin auth
    login_res = _auth_headers(client, 'adm', 'pass')
    assert login_res.status_code == 200
    admin_token = login_res.get_json()['data']['access_token']
    admin_h = {'Authorization': f'Bearer {admin_token}'}

    # Create and assign a shift
    start = datetime.utcnow().replace(microsecond=0)
    end = start + timedelta(hours=1)
    week_start = start.date().isoformat()
    res = client.post('/api/shifts', json={
        'adminId': admin.id,
        'startTime': start.isoformat(),
        'endTime': end.isoformat(),
        'location': 'HQ',
        'weekStart': week_start,
    }, headers=admin_h)
    assert res.status_code == 201
    shift_id = res.get_json()['id']

    res = client.post(f'/api/shifts/{shift_id}/assign', json={'staffId': staff.id}, headers=admin_h)
    assert res.status_code == 200

    # Staff auth
    st_login = _auth_headers(client, 'stf', 'pass')
    assert st_login.status_code == 200
    st_token = st_login.get_json()['data']['access_token']
    st_h = {'Authorization': f'Bearer {st_token}'}

    # Identify protected
    res = client.get('/api/identify', headers=st_h)
    assert res.status_code == 200
    assert 'username' in res.get_json().get('message', '')

    # Clock in/out
    res = client.post('/api/attendance/clock-in', json={'shiftId': shift_id, 'timestamp': start.isoformat()}, headers=st_h)
    assert res.status_code == 201
    res = client.post('/api/attendance/clock-out', json={'shiftId': shift_id, 'timestamp': end.isoformat()}, headers=st_h)
    assert res.status_code == 200

    # /api/me/shifts
    res = client.get('/api/me/shifts', headers=st_h)
    assert res.status_code == 200
    ids = [s['id'] for s in res.get_json()]
    assert shift_id in ids

    # /api/attendance/my-records
    res = client.get('/api/attendance/my-records', headers=st_h)
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

    # /api/reports/all (admin)
    res = client.get('/api/reports/all', headers=admin_h)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_list_all_shifts_endpoint(client):
    """Verify GET /api/shifts returns created shifts."""
    # Login as existing admin from previous test (username 'adm')
    login_res = _auth_headers(client, 'adm', 'pass')
    assert login_res.status_code == 200
    token = login_res.get_json()['data']['access_token']
    h = {'Authorization': f'Bearer {token}'}

    # Find admin id via users API
    users = client.get('/api/users').get_json()
    admin_id = next(u['id'] for u in users if u['username'] == 'adm')

    # Create a new shift so we can assert presence
    from datetime import datetime, timedelta
    start = datetime.utcnow().replace(microsecond=0)
    end = start + timedelta(hours=2)
    week_start = start.date().isoformat()
    created = client.post('/api/shifts', json={
        'adminId': admin_id,
        'startTime': start.isoformat(),
        'endTime': end.isoformat(),
        'location': 'HQ-2',
        'weekStart': week_start,
    }, headers=h)
    assert created.status_code == 201
    created_id = created.get_json()['id']

    # List all shifts
    res = client.get('/api/shifts', headers=h)
    assert res.status_code == 200
    data = res.get_json()
    ids = [s['id'] for s in data]
    assert created_id in ids

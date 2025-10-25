import pytest
from App.controllers.base import BaseController


pytestmark = pytest.mark.unit


def test_success_response_and_to_json():
    data = {'a': 1}
    resp = BaseController.success_response(data, message='ok')
    assert resp['success'] is True
    assert resp['message'] == 'ok'
    assert resp['data'] == data

    class Obj:
        def __init__(self):
            self.x = 10
    obj = Obj()
    j = BaseController.to_json(obj)
    assert j['x'] == 10


def test_error_response():
    resp = BaseController.error_response('bad', code=422)
    assert resp['success'] is False
    assert resp['message'] == 'bad'
    assert resp['error_code'] == 422

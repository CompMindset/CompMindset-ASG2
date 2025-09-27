from datetime import datetime
from App.database import db
from App.models import Request

def make_request(staff_id:int, admin_id:int, req_type:str, reason:str="", shift_id:int=None):
    t = req_type.upper()
    if t not in ("SWAP","TIME-OFF"):
        raise ValueError("Invalid request type")
    r = Request(
        requestingStaffID=staff_id,
        assignedAdminID=admin_id,
        type=t,
        reason=reason,
        target_shift_id=shift_id
    )
    db.session.add(r)
    db.session.commit()
    return r

def decide_request(request_id:int, decision:str):
    d = decision.upper()
    if d not in ("APPROVED","REJECTED"):
        raise ValueError("Invalid decision")
    r = Request.query.get(request_id)
    if not r:
        raise ValueError("Request not found")
    r.status = d
    r.decidedAt = datetime.utcnow()
    db.session.commit()
    return r

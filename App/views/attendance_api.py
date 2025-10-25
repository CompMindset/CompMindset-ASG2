from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers import (
    clock_in,
    clock_out
)

attendance_api = Blueprint('attendance_api', __name__)

@attendance_api.route('/api/attendance/clock-in', methods=['POST'])
@jwt_required()
def clock_in_endpoint():
    """Staff clocks in for a shift"""
    data = request.json
    try:
        user = jwt_current_user
        attendance = clock_in(
            shift_id=data['shiftId'],
            staff_id=user.id,
            ts_iso=data['timestamp']
        )
        return jsonify({
            'id': attendance.id,
            'shiftId': attendance.shift_id,
            'staffId': attendance.staff_id,
            'clockIn': str(attendance.clockIn),
            'status': attendance.status,
            'message': 'Clocked in successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@attendance_api.route('/api/attendance/clock-out', methods=['POST'])
@jwt_required()
def clock_out_endpoint():
    """Staff clocks out from a shift"""
    data = request.json
    try:
        user = jwt_current_user
        attendance = clock_out(
            shift_id=data['shiftId'],
            staff_id=user.id,
            ts_iso=data['timestamp']
        )
        
        # Calculate hours worked
        hours_worked = None
        if attendance.clockIn and attendance.clockOut:
            delta = attendance.clockOut - attendance.clockIn
            hours_worked = round(delta.total_seconds() / 3600, 2)
        
        return jsonify({
            'id': attendance.id,
            'shiftId': attendance.shift_id,
            'staffId': attendance.staff_id,
            'clockIn': str(attendance.clockIn),
            'clockOut': str(attendance.clockOut),
            'hoursWorked': hours_worked,
            'status': attendance.status,
            'message': 'Clocked out successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@attendance_api.route('/api/attendance/my-records', methods=['GET'])
@jwt_required()
def get_my_attendance_endpoint():
    """Staff gets their attendance records"""
    try:
        from App.models import Attendance
        from App.database import db
        
        user = jwt_current_user
        records = db.session.execute(
            db.select(Attendance).filter_by(staff_id=user.id)
        ).scalars().all()
        
        result = []
        for r in records:
            # Calculate hours worked
            hours_worked = None
            if r.clockIn and r.clockOut:
                delta = r.clockOut - r.clockIn
                hours_worked = round(delta.total_seconds() / 3600, 2)
            
            result.append({
                'id': r.id,
                'shiftId': r.shift_id,
                'clockIn': str(r.clockIn),
                'clockOut': str(r.clockOut) if r.clockOut else None,
                'hoursWorked': hours_worked,
                'status': r.status
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

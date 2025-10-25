from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers import (
    create_shift,
    assign_shift,
    publish_roster,
    list_all_shifts
)

shift_api = Blueprint('shift_api', __name__)

@shift_api.route('/api/shifts', methods=['POST'])
@jwt_required()
def create_shift_endpoint():
    """Admin creates a new shift"""
    data = request.json
    try:
        shift = create_shift(
            admin_id=data['adminId'],
            start_iso=data['startTime'],
            end_iso=data['endTime'],
            location=data['location'],
            week_start_iso=data['weekStart']
        )
        return jsonify({
            'id': shift.id,
            'adminId': shift.admin_id,
            'startTime': str(shift.start_time),
            'endTime': str(shift.end_time),
            'location': shift.location,
            'weekStart': str(shift.week_start),
            'status': shift.status
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@shift_api.route('/api/shifts', methods=['GET'])
@jwt_required()
def get_all_shifts_endpoint():
    """Get all shifts"""
    try:
        shifts = list_all_shifts()
        return jsonify([{
            'id': s.id,
            'adminId': s.admin_id,
            'staffId': s.staff_id,
            'startTime': str(s.start_time),
            'endTime': str(s.end_time),
            'location': s.location,
            'weekStart': str(s.week_start),
            'status': s.status
        } for s in shifts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@shift_api.route('/api/shifts/<int:shift_id>/assign', methods=['POST'])
@jwt_required()
def assign_shift_endpoint(shift_id):
    """Admin assigns a shift to staff"""
    data = request.json
    try:
        shift = assign_shift(shift_id, data['staffId'])
        return jsonify({
            'message': f"Shift {shift_id} assigned to staff {data['staffId']}",
            'shiftId': shift.id,
            'staffId': shift.staff_id,
            'status': shift.status
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@shift_api.route('/api/roster/publish', methods=['POST'])
@jwt_required()
def publish_roster_endpoint():
    """Admin publishes roster for a week"""
    data = request.json
    try:
        shifts = publish_roster(data['weekStart'])
        return jsonify({
            'message': f"Roster published for week {data['weekStart']}",
            'shifts': [{
                'id': s.id,
                'staffId': s.staff_id,
                'startTime': str(s.start_time),
                'endTime': str(s.end_time),
                'location': s.location,
                'status': s.status
            } for s in shifts]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@shift_api.route('/api/me/shifts', methods=['GET'])
@jwt_required()
def get_my_shifts_endpoint():
    """Staff gets their own shifts"""
    week = request.args.get('week')
    try:
        from App.models import Shift
        from App.database import db
        
        user = jwt_current_user
        query = db.select(Shift).filter_by(staff_id=user.id)
        
        if week:
            query = query.filter_by(week_start=week)
        
        shifts = db.session.execute(query).scalars().all()
        
        return jsonify([{
            'id': s.id,
            'startTime': str(s.start_time),
            'endTime': str(s.end_time),
            'location': s.location,
            'weekStart': str(s.week_start),
            'status': s.status
        } for s in shifts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

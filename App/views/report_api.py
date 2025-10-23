from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from App.controllers import (
    generate_weekly_report
)

report_api = Blueprint('report_api', __name__)

@report_api.route('/api/reports/weekly', methods=['GET'])
@jwt_required()
def get_weekly_report_endpoint():
    """Admin gets weekly report"""
    week_start = request.args.get('weekStart')
    try:
        report = generate_weekly_report(week_start)
        return jsonify({
            'id': report.id,
            'weekStart': str(report.weekStart),
            'totalShifts': report.totalShifts,
            'totalHours': float(report.totalHours),
            'generatedAt': str(report.generatedAt)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@report_api.route('/api/reports/all', methods=['GET'])
@jwt_required()
def get_all_reports_endpoint():
    """Admin gets all reports"""
    try:
        from App.models import Report
        from App.database import db
        
        reports = db.session.execute(db.select(Report)).scalars().all()
        
        return jsonify([{
            'id': r.id,
            'weekStart': str(r.weekStart),
            'totalShifts': r.totalShifts,
            'totalHours': float(r.totalHours),
            'generatedAt': str(r.generatedAt)
        } for r in reports]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

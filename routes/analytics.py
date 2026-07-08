from flask import Blueprint, jsonify

from services.analytics_service import AnalyticsService

analytics = Blueprint("analytics", __name__)


@analytics.route("/api/analytics/departments")
def department_chart():

    return jsonify(
        AnalyticsService.department_chart_data()
    )


@analytics.route("/api/analytics/gender")
def gender_chart():

    return jsonify(
        AnalyticsService.gender_chart_data()
    )


@analytics.route("/api/analytics/semester")
def semester_chart():

    return jsonify(
        AnalyticsService.semester_chart_data()
    )


@analytics.route("/api/analytics/attendance")
def attendance_chart():

    return jsonify(
        AnalyticsService.attendance_chart_data()
    )

@analytics.route("/api/analytics/cgpa")
def cgpa_chart():

    return jsonify(
        AnalyticsService.cgpa_chart_data()
    )

@analytics.route("/api/analytics/performance")
def performance_chart():

    return jsonify(
        AnalyticsService.performance_chart_data()
    )

@analytics.route("/api/analytics/kpi")
def kpi_data():

    return jsonify(
        AnalyticsService.kpi_data()
    )

@analytics.route("/api/analytics/top_students")
def top_students():

    return jsonify(
        AnalyticsService.top_students()
    )

@analytics.route("/api/analytics/at_risk")
def at_risk_students():

    return jsonify(
        AnalyticsService.at_risk_students()
    )
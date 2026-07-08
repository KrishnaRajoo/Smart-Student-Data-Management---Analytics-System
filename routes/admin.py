from flask import Blueprint, render_template

from models.student import Student
from models.teacher import Teacher
from models.department import Department
from services.analytics_service import AnalyticsService

admin = Blueprint("admin", __name__)

@admin.route("/admin/dashboard")
def dashboard():

    stats = AnalyticsService.dashboard_statistics()

    return render_template(

        "admin/dashboard.html",

        stats=stats

    )

@admin.route("/admin/analytics")
def analytics():

    return render_template(

        "admin/analytics.html"

    )

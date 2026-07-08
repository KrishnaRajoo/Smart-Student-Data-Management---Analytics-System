from flask import Blueprint

student = Blueprint("student", __name__)

@student.route("/student/dashboard")
def dashboard():
    return "<h1>Student Dashboard</h1>"
from flask import Blueprint, render_template, session, redirect, url_for

from models.teacher import Teacher
from models.student import Student

teacher = Blueprint("teacher", __name__)


@teacher.route("/teacher/dashboard")
def dashboard():

    if session.get("role") != "teacher":

        return redirect(
            url_for("auth.login", role="teacher")
        )

    teacher_data = Teacher.query.get(
        session["teacher_id"]
    )

    total_students = Student.query.filter_by(
        department_id=teacher_data.department_id
    ).count()

    return render_template(

        "teacher/dashboard.html",

        teacher=teacher_data,

        total_students=total_students

    )
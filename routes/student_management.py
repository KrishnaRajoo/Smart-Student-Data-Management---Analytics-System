from flask import Blueprint, render_template
from models.student import Student
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import db
from models.student import Student
from models.department import Department
from services.student_service import StudentService
from sqlalchemy import or_

student_management = Blueprint(
    "student_management",
    __name__
)

@student_management.route("/admin/students")
def students():

    search = request.args.get("search", "")

    department = request.args.get("department", "")

    semester = request.args.get("semester", "")

    page = request.args.get("page", 1, type=int)

    query = Student.query

    from sqlalchemy import or_

    if search:

        query = query.filter(

            or_(

                Student.student_id.ilike(f"%{search}%"),

                Student.first_name.ilike(f"%{search}%"),

                Student.last_name.ilike(f"%{search}%")

            )

        )

    if department:

        query = query.filter(
            Student.department_id == int(department)
        )

    if semester:

        query = query.filter(
            Student.semester == int(semester)
        )

    students = query.order_by(
        Student.student_id
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    return render_template(

        "admin/students.html",

        students=students,

        departments=departments,

        search=search,

        department=department,

        semester=semester

    )

@student_management.route("/admin/students/add", methods=["GET", "POST"])
def add_student():

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

        StudentService.create_student(request.form)

        flash("Student added successfully!", "success")

        return redirect(
            url_for("student_management.students")
        )

    return render_template(

        "admin/add_student.html",

        departments=departments

    )

@student_management.route(
    "/admin/students/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_student(id):

    student = StudentService.get_student(id)

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if student is None:

        flash("Student not found.", "danger")

        return redirect(
            url_for("student_management.students")
        )

    if request.method == "POST":

        student.first_name = request.form["first_name"]
        student.last_name = request.form["last_name"]
        student.email = request.form["email"]
        student.phone = request.form["phone"]
        student.gender = request.form["gender"]
        student.semester = int(request.form["semester"])
        student.cgpa = float(request.form["cgpa"])
        student.attendance = float(request.form["attendance"])
        student.department_id = int(request.form["department_id"])

        db.session.commit()

        flash("Student updated successfully!", "success")

        return redirect(
            url_for("student_management.students")
        )

    return render_template(
        "admin/edit_student.html",
        student=student,
        departments=departments
    )

@student_management.route("/admin/students/delete/<int:id>")
def delete_student(id):

    deleted = StudentService.delete_student(id)

    if deleted:

        flash("Student deleted successfully!", "success")

    else:

        flash("Student not found!", "danger")

    return redirect(
        url_for("student_management.students")
    )
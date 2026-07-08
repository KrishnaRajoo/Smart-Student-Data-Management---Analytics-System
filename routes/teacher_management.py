from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from database.db import db
from models.teacher import Teacher
from models.department import Department
from werkzeug.security import generate_password_hash


teacher_management = Blueprint(
    "teacher_management",
    __name__
)


@teacher_management.route("/admin/teachers")
def teachers():

    search = request.args.get("search", "")
    department = request.args.get("department", "")

    query = Teacher.query

    if search:

        query = query.filter(

            (Teacher.teacher_id.contains(search)) |

            (Teacher.first_name.contains(search)) |

            (Teacher.last_name.contains(search)) |

            (Teacher.email.contains(search))

        )

    if department:

        query = query.filter(
            Teacher.department_id == department
        )

    teachers = query.order_by(
        Teacher.first_name
    ).all()

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    return render_template(

        "admin/teachers.html",

        teachers=teachers,

        departments=departments,

        search=search,

        selected_department=department

    )

@teacher_management.route("/admin/teachers/add", methods=["GET", "POST"])
def add_teacher():

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

        teacher = Teacher(

            teacher_id=request.form["teacher_id"],

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            email=request.form["email"],

            phone=request.form.get("phone"),

            password=generate_password_hash(
                request.form["password"]
            ),

            gender=request.form.get("gender"),

            designation=request.form["designation"],

            qualification=request.form.get("qualification"),

            joining_date=datetime.strptime(
                request.form["joining_date"],
                "%Y-%m-%d"
            ).date() if request.form.get("joining_date") else None,

            status=request.form.get("status"),

            department_id=request.form["department_id"]

        )

        db.session.add(teacher)
        db.session.commit()

        flash("Teacher added successfully!", "success")

        return redirect(
            url_for("teacher_management.teachers")
        )

    return render_template(
        "admin/add_teacher.html",
        departments=departments
    )


@teacher_management.route(
    "/admin/teachers/edit/<int:teacher_id>",
    methods=["GET", "POST"]
)
def edit_teacher(teacher_id):

    teacher = Teacher.query.get_or_404(teacher_id)

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

        teacher.teacher_id = request.form["teacher_id"]

        teacher.first_name = request.form["first_name"]

        teacher.last_name = request.form["last_name"]

        teacher.email = request.form["email"]

        teacher.phone = request.form.get("phone")

        if request.form["password"]:

            teacher.password = generate_password_hash(
                request.form["password"]
            )

        teacher.gender = request.form.get("gender")

        teacher.designation = request.form["designation"]

        teacher.qualification = request.form.get("qualification")

        teacher.joining_date = (
            datetime.strptime(
                request.form["joining_date"],
                "%Y-%m-%d"
            ).date()
            if request.form.get("joining_date")
            else None
        )

        teacher.status = request.form.get("status")

        teacher.department_id = request.form["department_id"]

        db.session.commit()

        flash(
            "Teacher updated successfully!",
            "success"
        )

        return redirect(
            url_for("teacher_management.teachers")
        )

    return render_template(
        "admin/edit_teacher.html",
        teacher=teacher,
        departments=departments
    )
@teacher_management.route("/admin/teachers/delete/<int:teacher_id>")
def delete_teacher(teacher_id):

    teacher = Teacher.query.get_or_404(teacher_id)

    db.session.delete(teacher)

    db.session.commit()

    flash("Teacher deleted successfully!", "success")

    return redirect(
        url_for("teacher_management.teachers")
    )
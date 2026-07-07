from app import app
from database.db import db
from models.department import Department

with app.app_context():

    departments = [

        Department(
            department_code="CSE",
            department_name="Computer Science & Engineering",
            hod_name="Dr. A. Sharma"
        ),

        Department(
            department_code="AIDS",
            department_name="Artificial Intelligence & Data Science",
            hod_name="Dr. P. Singh"
        ),

        Department(
            department_code="ECE",
            department_name="Electronics & Communication",
            hod_name="Dr. S. Verma"
        ),

        Department(
            department_code="ME",
            department_name="Mechanical Engineering",
            hod_name="Dr. R. Kumar"
        )

    ]

    for department in departments:

        exists = Department.query.filter_by(
            department_code=department.department_code
        ).first()

        if not exists:

            db.session.add(department)

    db.session.commit()

    print("Departments added successfully.")
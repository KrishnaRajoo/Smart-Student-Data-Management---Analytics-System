from faker import Faker
import random

from app import app
from database.db import db

from models.student import Student
from models.department import Department

fake = Faker("en_IN")

with app.app_context():

    departments = Department.query.all()

    if not departments:

        print("No departments found. Run seed_database.py first.")
        exit()

    if Student.query.count() > 0:
        print("Students already exist.")
        exit()

    for i in range(1, 101):

        department = random.choice(departments)

        student = Student(

            student_id=f"ST{i:03}",

            first_name=fake.first_name(),

            last_name=fake.last_name(),

            email=f"student{i}@college.edu",

            phone=fake.phone_number(),

            gender=random.choice(["Male", "Female"]),

            semester=random.randint(1, 8),

            cgpa=round(random.uniform(6.0, 9.9), 2),

            attendance=round(random.uniform(70, 100), 2),

            department_id=department.id

        )

        db.session.add(student)

    db.session.commit()

    print("100 students added successfully!")
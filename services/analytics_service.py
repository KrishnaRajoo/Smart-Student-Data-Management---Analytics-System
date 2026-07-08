from sqlalchemy import func

from sqlalchemy import case

from models.student import Student
from models.teacher import Teacher
from models.department import Department
from database.db import db
from models.attendance import Attendance

from sqlalchemy import func



class AnalyticsService:

    @staticmethod
    def dashboard_statistics():

        total_students = Student.query.count()

        total_teachers = Teacher.query.count()

        total_departments = Department.query.count()

        average_cgpa = db.session.query(
            func.avg(Student.cgpa)
        ).scalar() or 0

        average_attendance = db.session.query(
            func.avg(Student.attendance)
        ).scalar() or 0

        return {

            "students": total_students,

            "teachers": total_teachers,

            "departments": total_departments,

            "cgpa": round(average_cgpa,2),

            "attendance": round(average_attendance,2)

        }
    @staticmethod
    def department_chart_data():

        data = (
            db.session.query(
                Department.department_name,
                func.count(Student.id)
            )
            .join(Student)
            .group_by(Department.department_name)
            .all()
        )

        return {

            "labels": [row[0] for row in data],

            "values": [row[1] for row in data]

        }
    @staticmethod
    def gender_chart_data():

        data = (
            db.session.query(
                Student.gender,
                func.count(Student.id)
            )
            .group_by(Student.gender)
            .all()
        )

        return {

            "labels": [row[0] for row in data],

            "values": [row[1] for row in data]

        }
    @staticmethod
    def semester_chart_data():

        data = (
            db.session.query(
                Student.semester,
                func.count(Student.id)
            )
            .group_by(Student.semester)
            .order_by(Student.semester)
            .all()
        )

        return {

            "labels": [f"Sem {row[0]}" for row in data],

            "values": [row[1] for row in data]

        }
    @staticmethod
    def attendance_chart_data():

        data = (
            db.session.query(
                Department.department_name,
                func.avg(Student.attendance)
            )
            .join(Student)
            .group_by(Department.department_name)
            .all()
        )

        return {

            "labels": [row[0] for row in data],

            "values": [round(row[1], 2) for row in data]

        }
    @staticmethod
    def cgpa_chart_data():

        data = (
            db.session.query(
                Department.department_name,
                func.avg(Student.cgpa)
            )
            .join(Student, Student.department_id == Department.id)
            .group_by(Department.department_name)
            .all()
        )

        return {

            "labels": [row[0] for row in data],

            "values": [round(row[1], 2) for row in data]

        }
    @staticmethod
    def performance_chart_data():

        excellent = Student.query.filter(Student.cgpa >= 9).count()

        good = Student.query.filter(
            Student.cgpa >= 8,
            Student.cgpa < 9
        ).count()

        average = Student.query.filter(
            Student.cgpa >= 7,
            Student.cgpa < 8
        ).count()

        improvement = Student.query.filter(
            Student.cgpa < 7
        ).count()

        return {

            "labels":[

                "Excellent",

                "Good",

                "Average",

                "Needs Improvement"

            ],

            "values":[

                excellent,

                good,

                average,

                improvement

            ]

        }
    @staticmethod
    def kpi_data():

        total_students = Student.query.count()

        total_teachers = Teacher.query.count()

        total_departments = Department.query.count()

        avg_cgpa = db.session.query(
            func.avg(Student.cgpa)
        ).scalar()

        avg_attendance = db.session.query(
            func.avg(Student.attendance)
        ).scalar()

        return {

            "students": total_students,

            "teachers": total_teachers,

            "departments": total_departments,

            "cgpa": round(avg_cgpa or 0, 2),

            "attendance": round(avg_attendance or 0, 2)

        }
    @staticmethod
    def top_students():

        students = (
            Student.query
            .order_by(Student.cgpa.desc(), Student.attendance.desc())
            .limit(10)
            .all()
        )

        result = []

        for student in students:

            result.append({

                "student_id": student.student_id,

                "department": student.department.department_name,

                "cgpa": student.cgpa,

                "attendance": student.attendance

            })

        return result
    @staticmethod
    def at_risk_students():

        students = Student.query.filter(

            (Student.attendance < 75) |
            (Student.cgpa < 7)

        ).all()

        result = []

        for student in students:

            if student.attendance < 75 and student.cgpa < 7:

                status = "Critical"

            else:

                status = "Warning"

            result.append({

                "student_id": student.student_id,

                "department": student.department.department_name,

                "attendance": student.attendance,

                "cgpa": student.cgpa,

                "status": status

            })

        return result

from flask import Flask, render_template

from config import Config
from database.db import db

from routes.auth import auth

from models.user import User
from models.department import Department
from models.student import Student
from models.teacher import Teacher
from models.attendance import Attendance

from routes.admin import admin
from routes.teacher import teacher
from routes.student import student
from routes.student_management import student_management
from routes.teacher_management import teacher_management
from routes.analytics import analytics

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(teacher)
app.register_blueprint(student)
app.register_blueprint(student_management)
app.register_blueprint(teacher_management)
app.register_blueprint(analytics)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
from app import app
from database.db import db
from models.user import User

with app.app_context():

    existing = User.query.filter_by(
        username="admin"
    ).first()

    if existing:

        print("Admin already exists.")

    else:

        admin = User(
            username="admin",
            role="admin"
        )

        admin.set_password("admin123")

        db.session.add(admin)

        db.session.commit()

        print("Admin account created successfully.")
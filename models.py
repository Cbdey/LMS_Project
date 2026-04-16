from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    email = db.Column(db.String(120), unique=True)

    password = db.Column(db.String(200))

    role = db.Column(db.String(20))

    is_verified = db.Column(db.Boolean, default=False)


class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    description = db.Column(db.Text)

    video = db.Column(db.String(200))

    notes = db.Column(db.String(200))

    instructor_id = db.Column(db.Integer)

    approved = db.Column(db.Boolean, default=False)


class Enrollment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer)

    course_id = db.Column(db.Integer)


# ===============================
# QUIZ TABLE
# ===============================

class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(db.Integer)

    question = db.Column(db.String(500))

    option1 = db.Column(db.String(200))

    option2 = db.Column(db.String(200))

    option3 = db.Column(db.String(200))

    option4 = db.Column(db.String(200))

    correct_answer = db.Column(db.String(200))


# ===============================
# QUIZ RESULT TABLE
# ===============================

class QuizResult(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer)

    course_id = db.Column(db.Integer)

    score = db.Column(db.Integer)
    

class VideoProgress(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, nullable=False)

    course_id = db.Column(db.Integer, nullable=False)

    progress = db.Column(db.Integer, default=0)
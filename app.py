from flask import Flask, render_template, redirect, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from config import Config
from models import db, User, Course, Enrollment, Quiz, QuizResult, VideoProgress

import os
import random
from datetime import datetime, timedelta


# ===============================
# APP CONFIG
# ===============================

app = Flask(__name__)
# ===============================
# MAIL CONFIGURATION (OTP EMAIL)
# ===============================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'deychandrabhanu6@gmail.com'

# Replace this with your Gmail App Password
app.config['MAIL_PASSWORD'] = 'dpwd eoir cvih emwt'

app.config['MAIL_DEFAULT_SENDER'] = 'deychandrabhanu6@gmail.com'

mail = Mail(app)
app.config.from_object(Config)


# ===============================
# UPLOAD FOLDER
# ===============================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ===============================
# DATABASE
# ===============================

db.init_app(app)


# ===============================
# LOGIN MANAGER
# ===============================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ===============================
# HOME
# ===============================

@app.route("/")
def home():
    return redirect("/login")


# ===============================
# REGISTER
# ===============================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered"

        otp = str(random.randint(100000, 999999))

        session["reg_username"] = username
        session["reg_email"] = email
        session["reg_password"] = generate_password_hash(password)
        session["reg_role"] = role
        session["reg_otp"] = otp
        session["reg_expiry"] = (datetime.now() + timedelta(minutes=5)).isoformat()


        # SEND OTP EMAIL
        msg = Message(
            "LMS Registration OTP",
            recipients=[email]
        )

        msg.body = f"Your LMS registration OTP is: {otp}"

        mail.send(msg)


        return redirect("/verify-registration-otp")

    return render_template("register.html")

@app.route("/verify-registration-otp", methods=["GET", "POST"])
def verify_registration_otp():

    if "reg_email" not in session:
        return redirect("/register")

    if request.method == "POST":

        entered_otp = request.form.get("otp")

        if entered_otp == session.get("reg_otp"):

            user = User(
    username=session["reg_username"],
    email=session["reg_email"],
    password=session["reg_password"],
    role=session["reg_role"],
    is_verified=True
)

            db.session.add(user)
            db.session.commit()

            session.clear()

            return redirect("/login")

        return "Invalid OTP"

    return render_template("verify_registration_otp.html")
@app.route("/resend-registration-otp")
def resend_registration_otp():

    if "reg_email" not in session:
        return redirect("/register")

    email = session["reg_email"]

    otp = str(random.randint(100000, 999999))

    session["reg_otp"] = otp
    session["reg_expiry"] = (
        datetime.now() + timedelta(minutes=5)
    ).isoformat()

    msg = Message(
        "LMS Registration OTP",
        recipients=[email]
    )

    msg.body = f"Your new LMS registration OTP is: {otp}"

    mail.send(msg)

    return redirect("/verify-registration-otp")
# ===============================
# LOGIN
# ===============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return "User not found"

        if not user.is_verified:
            return "Please verify your email before login"

        if check_password_hash(user.password, password):

            login_user(user)

            return redirect("/dashboard")

        return "Invalid login credentials"

    return render_template("login.html")


# ===============================
# FORGOT PASSWORD (OTP)
# ===============================

@app.route("/forgot-password", methods=["GET","POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return "Email not registered"

        otp = str(random.randint(100000,999999))

        session["reset_otp"] = otp
        session["reset_email"] = email
        session["otp_expiry"] = (datetime.now()+timedelta(minutes=5)).isoformat()


        # SEND EMAIL OTP HERE
        msg = Message(
            "LMS Password Reset OTP",
            recipients=[email]
        )

        msg.body = f"Your LMS password reset OTP is: {otp}"

        mail.send(msg)


        return redirect("/verify-otp")

    return render_template("forgot_password.html")


@app.route("/verify-otp", methods=["GET","POST"])
def verify_otp():

    if request.method == "POST":

        if request.form["otp"] == session.get("reset_otp"):

            return redirect("/reset-password")

        return "Invalid OTP"

    return render_template("verify_otp.html")


@app.route("/reset-password", methods=["GET","POST"])
def reset_password():

    if request.method == "POST":

        user = User.query.filter_by(email=session["reset_email"]).first()

        user.password = generate_password_hash(request.form["password"])

        db.session.commit()

        session.clear()

        return redirect("/login")

    return render_template("reset_password.html")


# ===============================
# DASHBOARD
# ===============================
@app.route("/dashboard")
@login_required
def dashboard():

    role = current_user.role

    if role == "student":

        enrolled_courses = Enrollment.query.filter_by(
            student_id=current_user.id
        ).count()

        progress_records = VideoProgress.query.filter_by(
            student_id=current_user.id
        ).all()

        completed_courses = sum(
            1 for record in progress_records if record.progress == 100
        )

        pending_courses = enrolled_courses - completed_courses

        certificates = completed_courses

        return render_template(
            "dashboard.html",
            role=role,
            enrolled_courses=enrolled_courses,
            completed_courses=completed_courses,
            pending_courses=pending_courses,
            certificates=certificates
        )


    if role == "instructor":

        instructor_courses = Course.query.filter_by(
            instructor_id=current_user.id
        ).count()

        instructor_students = Enrollment.query.count()

        instructor_quizzes = Quiz.query.count()

        pending_reviews = QuizResult.query.count()

        return render_template(
            "dashboard.html",
            role=role,
            instructor_courses=instructor_courses,
            instructor_students=instructor_students,
            instructor_quizzes=instructor_quizzes,
            pending_reviews=pending_reviews
        )


    if role == "admin":

        total_users = User.query.count()

        total_students = User.query.filter_by(role="student").count()

        total_instructors = User.query.filter_by(role="instructor").count()

        pending_courses = Course.query.filter_by(approved=False).count()

        return render_template(
            "dashboard.html",
            role=role,
            total_users=total_users,
            total_students=total_students,
            total_instructors=total_instructors,
            pending_courses=pending_courses
        )
# ===============================
# CREATE QUIZ (Instructor)
# ===============================

@app.route("/create-quiz", methods=["GET", "POST"])
@login_required
def create_quiz():

    if current_user.role != "instructor":
        return "Unauthorized access"

    courses = Course.query.filter_by(
        instructor_id=current_user.id
    ).all()

    if request.method == "POST":

        quiz = Quiz(
            course_id=request.form["course_id"],
            question=request.form["question"],
            option1=request.form["option1"],
            option2=request.form["option2"],
            option3=request.form["option3"],
            option4=request.form["option4"],
            correct_answer=request.form["correct_answer"]
        )

        db.session.add(quiz)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("create_quiz.html", courses=courses)


# ===============================
# ATTEMPT QUIZ (Student)
# ===============================

@app.route("/quiz/<int:course_id>", methods=["GET", "POST"])
@login_required
def attempt_quiz(course_id):

    quizzes = Quiz.query.filter_by(course_id=course_id).all()

    if request.method == "POST":

        score = 0

        for quiz in quizzes:

            selected = request.form.get(str(quiz.id))

            if selected == quiz.correct_answer:
                score += 1

        percentage = (score / len(quizzes)) * 100

        result = QuizResult(
            student_id=current_user.id,
            course_id=course_id,
            score=percentage
        )

        db.session.add(result)
        db.session.commit()

        return redirect("/progress")

    return render_template("quiz.html", quizzes=quizzes)


# ===============================
# PROGRESS PAGE (Student)
# ===============================

@app.route("/progress")
@login_required
def progress():

    results = db.session.query(
        QuizResult,
        Course.title
    ).join(
        Course,
        Course.id == QuizResult.course_id
    ).filter(
        QuizResult.student_id == current_user.id
    ).all()

    return render_template("progress.html", results=results)


# ===============================
# CERTIFICATE PAGE
# ===============================

@app.route("/certificate/<int:course_id>")
@login_required
def certificate(course_id):

    result = QuizResult.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    if not result or result.score < 50:
        return "Certificate available only after passing quiz"

    course = Course.query.get(course_id)

    return render_template(
        "certificate.html",
        course=course
    )


# ===============================
# EVALUATE STUDENTS (Instructor)
# ===============================

@app.route("/evaluate")
@login_required
def evaluate():

    if current_user.role != "instructor":
        return "Unauthorized access"

    results = db.session.query(
        User.username,
        Course.title,
        QuizResult.score
    ).join(
        User,
        User.id == QuizResult.student_id
    ).join(
        Course,
        Course.id == QuizResult.course_id
    ).filter(
        Course.instructor_id == current_user.id
    ).all()

    return render_template("evaluate.html", results=results)


# ===============================
# MANAGE USERS (Admin)
# ===============================

@app.route("/manage-users")
@login_required
def manage_users():

    if current_user.role != "admin":
        return "Unauthorized access"

    users = User.query.all()

    return render_template("manage_users.html", users=users)


@app.route("/delete-user/<int:id>")
@login_required
def delete_user(id):

    if current_user.role != "admin":
        return "Unauthorized access"

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/manage-users")


# ===============================
# APPROVE COURSES (Admin)
# ===============================

@app.route("/approve-course")
@login_required
def approve_course():

    if current_user.role != "admin":
        return "Unauthorized access"

    courses = Course.query.all()

    return render_template(
        "approve_course.html",
        courses=courses
    )


@app.route("/approve/<int:id>")
@login_required
def approve(id):

    if current_user.role != "admin":
        return "Unauthorized access"

    course = Course.query.get_or_404(id)

    course.approved = True

    db.session.commit()

    return redirect("/approve-course")


# ===============================
# REPORTS PAGE (Admin)
# ===============================

@app.route("/reports")
@login_required
def reports():

    if current_user.role != "admin":
        return "Unauthorized access"

    total_users = User.query.count()
    total_courses = Course.query.count()
    total_results = QuizResult.query.count()

    return render_template(
        "reports.html",
        users=total_users,
        courses=total_courses,
        results=total_results
    )

# ===============================
# CREATE COURSE
# ===============================

@app.route("/create-course", methods=["GET","POST"])
@login_required
def create_course():

    if current_user.role!="instructor":
        return "Unauthorized"

    if request.method=="POST":

        video=request.files.get("video")
        notes=request.files.get("notes")

        video_name=None
        notes_name=None

        if video:
            video_name=secure_filename(video.filename)
            video.save(os.path.join(app.config["UPLOAD_FOLDER"],video_name))

        if notes:
            notes_name=secure_filename(notes.filename)
            notes.save(os.path.join(app.config["UPLOAD_FOLDER"],notes_name))

        db.session.add(Course(
            title=request.form["title"],
            description=request.form["description"],
            video=video_name,
            notes=notes_name,
            instructor_id=current_user.id
        ))

        db.session.commit()

        return redirect("/courses")

    return render_template("create_course.html")


# ===============================
# COURSES
# ===============================

@app.route("/courses")
@login_required
def courses():

    if current_user.role=="student":

        courses=Course.query.filter_by(approved=True).all()

    else:

        courses=Course.query.all()

    enrolled_ids=[]

    if current_user.role=="student":

        enrolled_ids=[e.course_id for e in Enrollment.query.filter_by(student_id=current_user.id)]

    return render_template("courses.html",courses=courses,enrolled_ids=enrolled_ids)


# ===============================
# ENROLL
# ===============================

@app.route("/enroll/<int:id>")
@login_required
def enroll(id):

    if current_user.role!="student":
        return "Students only"

    if not Enrollment.query.filter_by(student_id=current_user.id,course_id=id).first():

        db.session.add(Enrollment(student_id=current_user.id,course_id=id))

        db.session.commit()

    return redirect("/courses")


# ===============================
# LOGOUT
# ===============================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")


# ===============================
# RUN
# ===============================

if __name__=="__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
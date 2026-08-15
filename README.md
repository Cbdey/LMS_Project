# 📚 Learning Management System (LMS)

A comprehensive web-based Learning Management System built with Flask and SQLAlchemy. This platform enables educators to create and manage courses, conduct assessments, and track student progress while providing students with an interactive learning experience.

## ✨ Key Features

### 👤 User Management
- Secure registration and login with OTP email verification
- Role-based access control (Student, Instructor, Admin)
- Password reset functionality
- Email verification system

### 📖 Course Management
- Create and publish courses
- Upload course videos and study materials
- Admin approval workflow
- Student course enrollment
- Course dashboard and management

### 📝 Quiz & Assessment
- Create multiple-choice quizzes
- Auto-grade assessments
- Track quiz results and performance
- Question bank management

### 📊 Analytics & Progress
- Track student progress
- Performance reports
- Learning analytics dashboard
- Certificate generation

### 📧 Email Integration
- OTP-based verification
- Account notifications
- Password recovery emails
- Gmail SMTP integration

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask 3.1.0 |
| **Database** | SQLite + SQLAlchemy |
| **Authentication** | Flask-Login |
| **Email** | Flask-Mail (Gmail SMTP) |
| **Server** | Gunicorn |
| **Frontend** | HTML, CSS, Bootstrap, JavaScript |

## 📋 Prerequisites

- Python 3.7+
- pip
- Gmail account (for email features)

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/Cbdey/LMS_Project.git
cd LMS_Project
```

### 2. Virtual Environment
```bash
# Create
python -m venv venv

# Activate - Windows
venv\Scripts\activate

# Activate - Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Configuration
Edit `config.py`:
```python
class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 5. Email Configuration
Update `app.py` with your Gmail credentials:
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

### 6. Initialize Database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 7. Run Application
```bash
flask run
```
Application starts at: `http://localhost:5000`

## 📁 Folder Structure

```
LMS_Project/
├── app.py                      # Main application
├── config.py                   # Configuration
├── models.py                   # Database models
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── static/
│   ├── css/style.css
│   ├── js/
│   └── uploads/               # User files
└── templates/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── courses.html
    ├── create_course.html
    ├── quiz.html
    ├── progress.html
    ├── reports.html
    ├── certificate.html
    └── ...
```

## 🗄️ Database Schema

- **User** - Authentication & profiles
- **Course** - Course details & metadata
- **Enrollment** - Student course registrations
- **Quiz** - Quiz questions
- **QuizResult** - Student answers & scores
- **VideoProgress** - Learning tracking

## 💡 Usage Guide

### For Students
1. **Register** - Create account via registration page
2. **Verify Email** - Confirm email address with OTP
3. **Enroll** - Browse and enroll in available courses
4. **Learn** - Access course videos and materials
5. **Assess** - Complete quizzes to test knowledge
6. **Track Progress** - View learning progress and analytics
7. **Certify** - Download completion certificates

### For Instructors
1. **Login** - Access instructor dashboard
2. **Create Courses** - Upload course materials and videos
3. **Manage Content** - Edit and organize course content
4. **Create Assessments** - Add quizzes and evaluation questions
5. **Grade** - Evaluate student submissions
6. **Analytics** - View student performance metrics

### For Administrators
1. **Approve Courses** - Review and approve instructor courses
2. **Manage Users** - Handle user accounts and permissions
3. **Reports** - Generate system-wide analytics reports
4. **System Settings** - Configure system parameters

## � User Roles

| Role | Capabilities |
|------|-------------|
| **Student** | Enroll in courses, take quizzes, track progress, download certificates |
| **Instructor** | Create/manage courses, upload videos, create quizzes, view student performance |
| **Admin** | Approve courses, manage users, system reports, configuration |

## 🔐 Security

- Secure password hashing (Werkzeug)
- OTP email verification
- Session management
- CSRF protection
- Secure file uploads

## 📧 Email Setup

1. Generate Gmail App Password: https://support.google.com/accounts/answer/185833
2. Update credentials in `app.py`
3. Configure SMTP settings

## 📝 Main Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/register` | POST | User registration |
| `/login` | POST | User login |
| `/dashboard` | GET | User dashboard |
| `/courses` | GET | View courses |
| `/create_course` | POST | Create new course |
| `/quiz/<id>` | GET | Take quiz |
| `/progress` | GET | Track progress |
| `/reports` | GET | View analytics |

## 🌐 Live Demo

Coming soon after deployment...

## 🚀 Deployment

Deploy on:
- **Heroku** - Full backend support
- **Railway** - Python-friendly platform
- **Render** - Easy deployment

*Netlify is for frontend only; backend requires separate hosting*## 📧 Contact & Author

**Dey Chandrabhanu**  
📧 Email: deychandrabhanu6@gmail.com  
🔗 GitHub: [github.com/Cbdey](https://github.com/Cbdey)

---
**Version**: 1.0.0 | **Updated**: August 2026

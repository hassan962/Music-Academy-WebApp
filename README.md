# 🎵 Music Academy WebApp

A Django-based web platform for managing a digital music academy. Teachers can create and manage courses, upload video lessons, and schedule live classes. Students can enroll in courses, track their progress, and join upcoming live sessions — all through a responsive Bootstrap interface with dark mode support.

---

## ✨ Features

### 👩‍🏫 For Teachers:
- Create and manage courses
- Upload lesson videos and materials
- Schedule live classes with meeting links
- Access a dedicated teacher dashboard

### 👨‍🎓 For Students:
- Register and enroll in music courses
- Watch video lessons and mark them as completed
- Track lesson progress across all enrolled courses
- Join upcoming live classes directly from dashboard

### 🌙 UI / Experience:
- Responsive Bootstrap design
- Dark mode toggle
- Validation messages and success alerts using Django's message framework
- Background image support and transparent navbar

---

## ⚙️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite3
- **Media Handling:** Django File Uploads (for videos & PDFs)
- **Authentication:** Custom `AbstractUser` model with roles (teacher/student)

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/hassan962/Music-Academy-WebApp.git
cd Music-Academy-WebApp

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver

# UniVerse – Social Media Platform

<img src="static/images/universe-logo.png" alt="UniVerse Banner" width="300" height="150">

> **UniVerse** is a modern social media web application built with **Django** and **Tailwind CSS**, featuring secure authentication, user profiles, posts, social interactions, and notifications. Designed for learning **industry-standard backend and frontend workflows**.

---

## 🔹 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Setup & Installation](#setup--installation)
5. [Database Configuration](#database-configuration)
6. [Git Workflow](#git-workflow)
7. [Project Structure](#project-structure)
8. [Usage](#usage)
9. [Contribution](#contribution)
10. [License](#license)

---

## 📝 Project Overview

UniVerse is a **social media platform** with:

* Custom user authentication (register, login, logout, password reset)
* Extended user profiles (bio, image, education, experience, skills, social links)
* CRUD operations for posts (text + image)
* Follow / Unfollow system
* Feed displaying posts from followed users
* Like & Share functionality
* Direct messaging
* Notifications for key activities
* Responsive UI built with Tailwind CSS
* Secure, environment-variable-driven configuration

> Designed to mirror **real-world social media platforms** while teaching best practices in Django development.

---

## 🌟 Features

**Authentication**

* Register, Login, Logout
* Forgot Password / Reset Password (email-based)

**Profile**

* Bio, Profile Picture
* Personal Info: DOB, Location
* Professional Info: Education, Experience, Skills
* Social: Website URL

**Social**

* Post CRUD (text & image)
* Follow / Unfollow users
* Feed logic (followed users only)
* Like & Share posts

**Messaging & Notifications**

* Direct 1-to-1 messaging
* Real-time notification system using Django signals

**UI**

* Tailwind CSS for responsive and modern design
* Auth pages (`login`, `register`, `password reset`)
* Base layout template for consistent design

**Development**

* Docker support for Django + PostgreSQL
* Git feature-branch workflow
* Environment variables with `.env`

---

## 🛠 Tech Stack

| Layer      | Technology                           |
| ---------- | ------------------------------------ |
| Backend    | Django 6.x                           |
| Frontend   | Tailwind CSS, HTML, Django Templates |
| Database   | PostgreSQL                           |
| Dev Tools  | Git, Python 3.11+, pip, venv          |
| Deployment | Docker (optional)                    |
| Email      | Django console backend (development) |

---

## ⚡ Setup & Installation

**Clone the repository**

```bash
git clone https://github.com/<your-username>/universe-social-media.git
cd universe-social-media
```

**Create & activate virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Configure environment variables**

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key

DB_NAME=universe_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=no-reply@universe.com
```

---

## 🗄 Database Configuration

**Create PostgreSQL database**

```sql
CREATE DATABASE universe_db;
```

**Apply migrations**

```bash
python manage.py migrate
```

**Create superuser**

```bash
python manage.py createsuperuser
```

**Run development server**

```bash
python manage.py runserver
```

Access the app at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌳 Git Workflow

* **Main branches**

  * `main` → Production-ready
  * `develop` → Integration / testing

* **Feature branches**

  * `feature/<feature-name>` → Each module or fix
  * PR → Code review → merge into `develop` → merge `develop` → `main`

* **Commit messages**

```text
<feature>: short descriptive message
```

Example:

```text
auth-system: add register and login functionality
profile: add bio, experience, and social links
password-reset: implement forgot/reset password system
```

---

## 📂 Project Structure

```
universe-social-media/
├── accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   ├── views.py
│   └── templates/auth/
│       ├── login.html
│       ├── register.html
│       ├── password_reset.html
│       ├── password_reset_done.html
│       ├── password_reset_confirm.html
│       └── password_reset_complete.html
├── universe/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
├── templates/
│   ├── auth_base.html
│   └── base.html
├── venv/
├── manage.py
├── .env
└── requirements.txt
```

---

## ▶ Usage

* Register a new user
* Login with credentials
* Edit profile information
* Create and manage posts
* Follow / unfollow users
* View feed of followed users
* Use forgot/reset password when needed

---

## 🤝 Contribution

1. Fork the repository
2. Create a feature branch: `feature/<feature-name>`
3. Commit changes with meaningful messages
4. Push branch and open a Pull Request to `develop`
5. Code review → merge into `develop`
6. After testing, merge `develop` into `main`

---

## 📜 License

This project is **for educational purposes**.

---

## 👨‍💻 Team – UniVerse Developers

This project has been developed by a dedicated team of **BAUET students**:

| Name | Stack / Role |
|------|--------------|
| [Md Mahfuz Hossain](https://www.linkedin.com/in/muhammadmahfuzhossain/) | Full Stack |
| [Tirtho Saha](https://www.linkedin.com/in/your-linkedin/) | Frontend |
| [Israt Binte Elias](https://www.linkedin.com/in/your-linkedin/) | Frontend |
| [Sabrina Binty Akhtar](https://www.linkedin.com/in/sabrina-binty-akhtar-7617a1264) | Backend |
| [Mst. Rizoana Khatun](https://www.linkedin.com/in/your-linkedin/) | Backend |
| [Nafis Shahriar](https://www.linkedin.com/in/your-linkedin/) | Backend |

All team members are **students of Bangladesh Army University of Engineering & Technology**, collaborating to build this social media platform.

---





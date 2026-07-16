# 🚀 TaskFlow API

A production-ready **Task Management REST API** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

This project demonstrates modern backend development practices, including authentication, role-based authorization, workspace collaboration, activity logging, automated testing, and clean project architecture.

---

# ✨ Features

## 🔐 Authentication

* JWT Authentication
* Secure Login
* Protected Endpoints

## 👤 Users

* Register User
* User Authentication

## 🏢 Workspaces

* Create Workspace
* List User Workspaces

## 👥 Workspace Members

* Add Members
* Update Member Roles
* Remove Members
* Owner Permission Checks

## ✅ Tasks

* Create Task
* Update Task
* Delete Task (Soft Delete)
* Restore Deleted Task
* Task Details
* Pagination
* Search
* Filtering
* Task Assignment

## 💬 Comments

* Create Comments
* Edit Own Comments
* Delete Own Comments
* Retrieve Task Comments

## 📋 Activity Logs

Every important action is automatically logged.

Examples include:

* Task Created
* Task Updated
* Task Deleted
* Task Restored
* Comment Created
* Comment Updated
* Comment Deleted

---

# 🛠 Tech Stack

* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic
* Pydantic
* JWT Authentication
* Pytest

---

# 📁 Project Structure

```text
taskflow-api/
│
├── alembic/
├── app/
│   ├── auth/
│   ├── constants/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── dependencies.py
│   └── main.py
│
├── tests/
├── requirements.txt
├── alembic.ini
└── README.md
```

---

# 🧩 Architecture

The project follows a layered architecture:

```
Router
    ↓
Service
    ↓
Database (SQLAlchemy)
```

Each layer has a single responsibility:

* Routers handle HTTP requests.
* Services contain business logic.
* Models define database entities.
* Schemas validate requests and responses.

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/taskflow-api.git
```

Go to the project folder:

```bash
cd taskflow-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`.

Run database migrations:

```bash
alembic upgrade head
```

Start the server:

```bash
uvicorn app.main:app --reload
```

---

# 📖 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 🧪 Testing

Run all tests:

```bash
pytest
```

Current test suite:

* ✅ 49 Passing Tests

The project includes tests for:

* Authentication
* Users
* Workspaces
* Workspace Members
* Tasks
* Comments
* Activity Logs
* Authorization
* Validation
* Error Handling

---

# 🔒 Security

The API uses:

* JWT Authentication
* Password Hashing
* Role-Based Authorization
* Ownership Validation
* Workspace Membership Validation

---

# 📌 Future Improvements

Potential future enhancements:

* Refresh Tokens
* Email Verification
* Password Reset
* File Attachments
* Task Labels
* Task Priorities Dashboard
* Notifications
* Docker Support
* CI/CD Pipeline

---

# 👩‍💻 Author

**Rahaf Moualla**

Backend Developer focused on Python, FastAPI, SQLAlchemy, and ERP systems.

---

# 📄 License

This project is available for educational and portfolio purposes.

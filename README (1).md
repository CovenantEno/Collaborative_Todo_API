
# Collaborative Todo API

A RESTful API built with Django REST Framework (DRF) for managing Todos and Tasks, with JWT authentication.  
Supports full CRUD operations for Todos and Tasks, including **nested Tasks under Todos**.

---

## 🚀 Setup Instructions

### 1. Clone the Project
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create Virtual Environment
```bash
python -m venv env
# macOS / Linux
source env/bin/activate
# Windows
env\Scripts\activate
```

### 3. Ins Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

---

# Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
ACCESS_TOKEN_LIFETIME=30       # minutes
REFRESH_TOKEN_LIFETIME=1       # days
```

---

# API Endpoints

# Authentication (JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Get access & refresh token |
| POST | `/api/auth/token/refresh/` | Refresh access token |

---

# Todos Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos/` | List all todos |
| POST | `/api/todos/` | Create a new todo |
| GET | `/api/todos/<id>/` | Retrieve a single todo |
| PUT | `/api/todos/<id>/` | Update a todo |
| DELETE | `/api/todos/<id>/` | Delete a todo |

---

# Tasks Endpoints (Flat)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/<id>/` | Retrieve a single task |
| PUT | `/api/tasks/<id>/` | Update a task |
| DELETE | `/api/tasks/<id>/` | Delete a task |

---

# Nested Tasks Endpoints
All tasks belong to a specific Todo.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos/<todo_id>/tasks/` | List all tasks under a todo |
| POST | `/api/todos/<todo_id>/tasks/` | Create a task under that todo |
| GET | `/api/todos/<todo_id>/tasks/<task_id>/` | Retrieve a specific task |
| PUT | `/api/todos/<todo_id>/tasks/<task_id>/` | Update a task |
| DELETE | `/api/todos/<todo_id>/tasks/<task_id>/` | Delete a task |

---

## 🧪 Testing Instructions (Postman)

1. **Register a user** using `/api/auth/register/`.
2. **Login** to get the **access token**.
3. In Postman → Authorization → Bearer Token → paste the access token.
4. Test Todos endpoints: `/api/todos/`
5. Test Tasks endpoints: `/api/tasks/`
6. Test Nested Tasks endpoints: `/api/todos/<todo_id>/tasks/`

---

# Requirements (`requirements.txt`)

```
Django>=4.2
djangorestframework>=3.15
djangorestframework-simplejwt>=6.3
python-dotenv>=1.0
```
---

# Notes
- All endpoints require authentication except register & login.
- Tasks are now **nested under Todos**.
- JWT token lifetime is controlled by the `SIMPLE_JWT` settings in `settings.py`.

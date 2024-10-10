# Todo API

A RESTful API for managing tasks and comments using Django REST Framework and JWT authentication. This project provides user registration, login, task management, and commenting functionalities.

## Features

- User registration and authentication with JWT tokens
- Create, read, update, and delete tasks
- Add comments to tasks
- Filter tasks based on status and user
- Comprehensive API documentation with drf-spectacular

## Technologies Used

- Django
- Django REST Framework
- Simple JWT for authentication
- Django Filters
- drf-spectacular for API documentation

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- A PostgreSQL or SQLite database

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/alishermutalov/todoAPI.git
   cd todoAPI
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   If you're using SQLite, you can skip this step. For PostgreSQL, create a database and update your `settings.py` with the database credentials.

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server:**

   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/`.

## Usage

### API Endpoints

- **Authentication**
  - `POST /register/`: Register a new user
  - `POST /login/`: Log in a user and receive JWT tokens
  - `POST /refresh/`: Refresh the access token using the refresh token
  - `POST /logout/`: Log out a user

- **Tasks**
  - `GET /tasks/`: List all tasks (filtered by user)
  - `POST /task/create/`: Create a new task
  - `GET /task/detail/<int:pk>/`: Retrieve task details
  - `PATCH /task/update/<int:pk>/`: Update a task
  - `DELETE /task/delete/<int:pk>/`: Delete a task

- **Comments**
  - `GET /tasks/<int:task_id>/comments/`: List comments for a task
  - `POST /tasks/<int:task_id>/comments/create/`: Add a comment to a task

### Example Requests

**Register a User:**
```bash
curl -X POST http://127.0.0.1:8000/register/ -H "Content-Type: application/json" -d '{"username": "test_user", "password": "test_password", "password2": "test_password"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/login/ -H "Content-Type: application/json" -d '{"username": "test_user", "password": "test_password"}'
```

**Create a Task:**
```bash
curl -X POST http://127.0.0.1:8000/task/create/ -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"title": "New Task", "description": "Task description"}'
```

## API Documentation

The API is documented using [drf-spectacular](https://drf-spectacular.readthedocs.io/). You can access the documentation at:

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

